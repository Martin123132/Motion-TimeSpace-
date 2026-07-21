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

CHECKPOINT = "4600"
CLAIM_ID = "L-442"
BRANCH_ID = "MTS_R2FR_Y5_BOUNDARY_NONHILBERT_FINAL_CX_GATE_4600"
MARKER = "PPC4161_BOUNDARY_NONHILBERT_ZERO_OR_FINAL_CXLIVE_NORM_4600"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_NONHILBERT_ZERO_OR_FINAL_CXLIVE_NORM_4600"
DECISION = "BOUNDARY_NONHILBERT_ZERO_OR_FINAL_CX_LIVE_NORM_INSERTED_NONCLAIM"
NEXT_TARGET = "4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"

DOC_PATH = POST / "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
FORMAL_PATH = FORMAL / "616-PPC4161-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4600_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv"
FINAL_NORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_FINAL_CXLIVE_NORM.csv"
BODY_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_BODY_CHARGE_ENVELOPE_FINAL_CX_UPDATE.csv"
EMPIRICAL_INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_EMPIRICAL_SCORE_INPUT_INTERFACE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4600_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4600_VALIDATION.csv"

DOC_4599 = POST / "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"
FORMAL_615 = FORMAL / "615-PPC4161-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"
CSV_4599_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4599_NEXT_TARGET.csv"
CSV_4599_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4599_STATUS.csv"
CSV_4599_BODY = SOURCE_DIR / "P8_Y5_R2FR_4599_BODY_CHARGE_ENVELOPE_LABEL_HODGE_READOUT_UPDATE.csv"
CSV_4599_CXLIVE = SOURCE_DIR / "P8_Y5_R2FR_4599_CXLIVE_NEXT_NORM_ROWS.csv"
CSV_BOUNDARY_ZERO = SOURCE_DIR / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_BOUNDARY_ZERO_GATE.csv"
CSV_BOUNDARY_COUNTER = SOURCE_DIR / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_COUNTERMODEL_LEDGER.csv"
CSV_BOUNDARY_BOUND = SOURCE_DIR / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv"
CSV_BOUNDARY_REFERENCE = SOURCE_DIR / "P8_Y5_BOUNDARY_REFERENCE_CONDITIONAL_THEOREM_CHAIN.csv"
CSV_NO_SHADOW_2488 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2488_ZERO_THEOREM.csv"
CSV_NO_SHADOW_COUNTER = SOURCE_DIR / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv"
CSV_NH_2538 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2538_NONHILBERT_RESIDUAL_ROW.csv"
CSV_NH_4100 = SOURCE_DIR / "P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM.csv"
CSV_NH_3564_FALLBACK = SOURCE_DIR / "P8_Y5_R2FR_3564_OFFICIAL_NONHILBERT_FALLBACK_ROWS.csv"
CSV_NH_4431 = SOURCE_DIR / "P8_Y5_R2FR_4431_NONHILBERT_BYPASS_OUTPUT.csv"
CSV_SHADOW_4431 = SOURCE_DIR / "P8_Y5_R2FR_4431_SOURCE_SHADOW_OUTPUT.csv"
CSV_SHADOW_4432 = SOURCE_DIR / "P8_Y5_R2FR_4432_SHADOW_SPLIT_OUTPUT.csv"
CSV_KMSHADOW_4432 = SOURCE_DIR / "P8_Y5_R2FR_4432_KMSHADOW_VALUE_OUTPUT.csv"

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
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4600 completes the C_X live matter-trace leakage bookkeeping by deriving conditional boundary and non-Hilbert/shadow silence clauses, then inserting a final explicit C_X live norm when those clauses are not parent-signed.",
        "current_evidence": "Generated boundary/non-Hilbert zero theorem rows, final C_X live norm, updated A_mem/A_h body-charge envelopes, empirical-score interface rows, controls and validation.",
        "status": "boundary_nonHilbert_zero_or_final_CXlive_norm_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating imposed boundary conditions, exact improvements, covariance, Hilbert-current language or no-shadow slogans as if they prove compact boundary silence and total non-Hilbert source-current absence in one parent branch.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until the final body-charge vector B_X,C_X,J_X,Q_boundary_X,Z_X,M_X^2 and arena projections are parent-zero or source-backed below empirical bounds.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4600_00_4599_doc", DOC_4599, "C_X^post4599", "4599 live C_X handoff."),
        ("SRC4600_01_615_formal", FORMAL_615, "C_X^post4599", "formal 4599 C_X split."),
        ("SRC4600_02_4599_next", CSV_4599_NEXT, "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md", "machine-readable next target."),
        ("SRC4600_03_4599_status", CSV_4599_STATUS, "boundary/non-Hilbert C_X rows", "4599 status names the missing rows."),
        ("SRC4600_04_4599_body", CSV_4599_BODY, "BU4599_0_Csplit", "post4599 body-charge C split."),
        ("SRC4600_05_4599_cxlive", CSV_4599_CXLIVE, "C4599_4_LHRS", "LHRS live row."),
        ("SRC4600_06_boundary_zero", CSV_BOUNDARY_ZERO, "BZ2627_5_current_verdict", "boundary zero not parent-derived."),
        ("SRC4600_07_boundary_hair", CSV_BOUNDARY_COUNTER, "CM2627_3_boundary_hair", "boundary hair countermodel."),
        ("SRC4600_08_boundary_lift", CSV_BOUNDARY_BOUND, "RBP2627_2_boundary_lift", "finite boundary lift row."),
        ("SRC4600_09_boundary_gate", CSV_BOUNDARY_REFERENCE, "CT545_5_conditional_plateau", "boundary/reference conditional theorem."),
        ("SRC4600_10_no_shadow", CSV_NO_SHADOW_2488, "ZTH2488_2_current_verdict", "terminal public coframe no-shadow verdict."),
        ("SRC4600_11_no_shadow_counter", CSV_NO_SHADOW_COUNTER, "CM2488_2_source_prefactor", "source-prefactor countermodel."),
        ("SRC4600_12_nh_residual", CSV_NH_2538, "NHR2538_0_total", "non-Hilbert residual envelope."),
        ("SRC4600_13_nh_total", CSV_NH_4100, "NHB4100_2_total_zero_conditions", "non-Hilbert total zero conditions."),
        ("SRC4600_14_nh_failure", CSV_NH_4100, "NHB4100_3_live_failure", "live non-Hilbert failure."),
        ("SRC4600_15_nh_fallback", CSV_NH_3564_FALLBACK, "FNH3564_0_total", "official non-Hilbert fallback."),
        ("SRC4600_16_nh_4431", CSV_NH_4431, "NH4431_3_official_fallback_status", "recent non-Hilbert fallback validation."),
        ("SRC4600_17_shadow_4431", CSV_SHADOW_4431, "SH4431_3_source_shadow_current_verdict", "source-shadow verdict."),
        ("SRC4600_18_shadow_split", CSV_SHADOW_4432, "SPLIT4432_3_readout_projector_shadow", "source-shadow split."),
        ("SRC4600_19_kmshadow", CSV_KMSHADOW_4432, "KM4432_4_original_Kmshadow_bound_target", "shadow product bound target."),
        ("SRC4600_20_claim_441", CLAIMS_PATH, "L-441", "claim-register handoff from 4599."),
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


def zero_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "BNH4600_0_boundary_variation",
            "target": "C_X^boundary",
            "conditional_zero_route": "the parent variational principle fixes the X boundary data or zero flux/topological class, the improvement/reference form is exact with no compact representative, and no wall/domain selector stress is varied",
            "formula": "delta_X S_boundary=0 and Pi_local J_boundary_X=0 => C_X^boundary=0",
            "finite_fallback": "|C_X^boundary T| <= ||Pi_local J_boundary_X|| + ||boundary_lift_X|| + ||wall_stress_X|| + ||Delta_symp_X||",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED_BOUND_ROW_REQUIRED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "BNH4600_1_nonHilbert_decomposition",
            "target": "C_X^nonHilbert",
            "conditional_zero_route": "after Hilbert source extraction, spin/torsion, boundary/worldtube, improvement, readout reentry, shadow/projector and decoupled conserved source blocks are each absent, exact, or locally projection-silent in the same branch",
            "formula": "P_source[J_NH]=0 => C_X^nonHilbert=0",
            "finite_fallback": "|C_X^nonHilbert T| <= E_spin + E_boundary + E_improvement + E_readout + E_shadow_projector + E_decoupled",
            "current_status": "TOTAL_ZERO_CONDITIONAL_OFFICIAL_FALLBACK_ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "BNH4600_2_shadow_split",
            "target": "source-shadow subblock of C_X^nonHilbert",
            "conditional_zero_route": "pure source-only shadow vanishes if total Hilbert source owner is parent-signed; action-scale, hidden-marker and readout-projector survivors are reassigned to explicit live C sectors",
            "formula": "C_shadow_pure_source_only=0, while C_shadow_total -> C_action_scale + C_hidden_return + C_readout_projector unless their gates close",
            "finite_fallback": "|K_m_shadow C_shadow_total| kept as a nonclaim bound target until all subblocks are zero or numeric",
            "current_status": "PURE_SOURCE_ZERO_CONTRACT_READY_SURVIVORS_RETAINED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "BNH4600_3_combined_boundary_nonHilbert",
            "target": "C_X^boundary_nonHilbert_live",
            "conditional_zero_route": "BNH4600_0 and BNH4600_1 hold in the same parent branch, with no calibration hiding or cancellation between channels",
            "formula": "C_X^boundary_nonHilbert_live = C_X^boundary + C_X^nonHilbert = 0",
            "finite_fallback": "|C_X^boundary_nonHilbert_live| <= |C_X^boundary| + |C_X^nonHilbert|",
            "current_status": "COMBINED_ZERO_OR_ABSOLUTE_SUM_READY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "BNH4600_4_final_CX_live",
            "target": "C_X^final_live",
            "conditional_zero_route": "all post4598 standard/weight, post4599 LHRS, and 4600 boundary/non-Hilbert blocks vanish or have source-backed values below arena bounds",
            "formula": "C_X^final_live = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary_nonHilbert_live",
            "finite_fallback": "|C_X^final_live| <= |C_X^std_weight_live| + |C_X^LHRS_live| + |C_X^boundary| + |C_X^nonHilbert|",
            "current_status": "FINAL_CX_LIVE_NORM_INSERTED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def final_norm_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("C4600_0_boundary", "C_X^boundary", "boundary/reference/domain-wall leakage into matter-trace coupling", "prove parent boundary neutrality and compact local projection silence", "Delta_boundary_X"),
        ("C4600_1_nonHilbert", "C_X^nonHilbert", "non-Hilbert source-current bypass leakage", "prove P_source[J_NH]=0 componentwise in same branch", "epsilon_current_owner_NH_abs"),
        ("C4600_2_shadow_projector", "E_shadow_projector", "shadow/projector/support source-current tail inside non-Hilbert envelope", "prove terminal public coframe/source-shadow no-return and projector silence", "K_m_shadow*C_shadow_total"),
        ("C4600_3_boundary_nonHilbert", "C_X^boundary_nonHilbert_live", "combined boundary plus non-Hilbert live coefficient", "zero C4600_0 and C4600_1 in same branch", "absolute sum C4600_0+C4600_1"),
        ("C4600_4_final", "C_X^final_live", "final matter-trace coupling coefficient for memory/fibre body charge", "zero or source-bound all standard/weight/LHRS/boundary/non-Hilbert blocks", "absolute sum post4598+post4599+4600 live blocks"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": coeff_id,
            "symbol": symbol,
            "role": role,
            "derive_first": derive,
            "finite_fallback": fallback,
            "current_status": "MISSING_PARENT_ZERO_OR_VALUE" if coeff_id != "C4600_4_final" else "FINAL_CX_LIVE_NORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for coeff_id, symbol, role, derive, fallback in rows
    ]


def body_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4600_0_Csplit_final",
            "target": "C_X live after 4600",
            "formula": "C_X^final_live = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary_nonHilbert_live",
            "zero_condition": "C_X^final_live=0 only if all standard/weight, LHRS, boundary and non-Hilbert subblocks vanish in the same parent branch",
            "finite_bound": "|C_X^final_live| <= |C_X^std_weight_live|+|C_X^LHRS_live|+|C_X^boundary|+|C_X^nonHilbert|",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4600_1_memory",
            "target": "A_mem",
            "formula": "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs|| + ||C_mem^final_live||||T|| + ||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)",
            "zero_condition": "B_mem_eff=C_mem^final_live=J_mem_live=Q_boundary_mem=0",
            "finite_bound": "C_mem^boundary and C_mem^nonHilbert now enter through C_mem^final_live; Q_boundary_mem remains a separate Green-function boundary charge",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4600_2_fibre",
            "target": "A_h",
            "formula": "|A_h| <= [exp(R/lambda_h) int_body (||B_h||||R_obs|| + ||C_h^final_live||||T|| + ||J_h_live||) dV + ||Q_boundary_h||]/(4*pi||Z_h||)",
            "zero_condition": "B_h=C_h^final_live=J_h_live=Q_boundary_h=0",
            "finite_bound": "C_h^boundary and C_h^nonHilbert now enter through C_h^final_live; Q_boundary_h remains a separate Green-function boundary charge",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4600_3_boundary_separation",
            "target": "boundary bookkeeping",
            "formula": "C_X^boundary is matter-trace/source-coupling leakage; Q_boundary_X is exterior Green-function boundary charge",
            "zero_condition": "both must be zero or bounded separately; one cannot be used as a calibration sink for the other",
            "finite_bound": "|A_X| keeps both ||C_X^final_live||||T|| and ||Q_boundary_X|| terms",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def empirical_interface_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("E4600_0_R10", "R10/short-range fifth force", "Z_X;M_X^2;lambda_X;B_X_eff;C_X^final_live;J_X_live;Q_boundary_X;K_R10", "alpha(lambda) prediction or theorem-zero certificate"),
        ("E4600_1_PPN", "PPN/local-GR vector", "Z_X;M_X^2;B_X_eff;C_X^final_live;J_X_live;Q_boundary_X;K_gamma,K_beta,K_alpha_i,K_xi,K_Gdot", "bounded residual vector compared with GR/PPN limits"),
        ("E4600_2_clock_WEP", "clock/WEP/source universality", "C_X^final_live;E_shadow_projector;C_standard_weight;readout kernels;material sensitivities", "clock/WEP response rows with units and source paths"),
        ("E4600_3_orbital_GM", "orbital/GM/light-time", "Q_boundary_X;Delta_symp_X;J_boundary_X;C_X^final_live;GM calibration rule", "orbital residual not absorbed into fitted GM"),
        ("E4600_4_EM_Poynting", "EM/Poynting/local energy flow", "J_EM_open;Delta_Hodge_EM_X;Poynting source leg;C_X^Hodge;C_X^final_live", "EM/Poynting contribution either theorem-owned or bounded"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "interface_id": row_id,
            "arena": arena,
            "required_inputs": required,
            "score_object": score,
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for row_id, arena, required, score in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4600_imposed_boundary",
            "input_branch": "Dirichlet/Neumann boundary condition imposed as a closure rather than derived from parent action",
            "expected": "C_X^boundary may be conditionally zero but remains nonclaim unless parent-selected",
            "status": "COUNTERMODEL_CAUGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4600_boundary_hair",
            "input_branch": "boundary primitive, wall stress, endpoint or domain selector carries local source hair",
            "expected": "C_X^boundary and/or Q_boundary_X remains live",
            "status": "COUNTERMODEL_CAUGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4600_exact_improvement_flux",
            "input_branch": "exact dmu improvement exists but compact flux/corner/readout dependence is not zero",
            "expected": "non-Hilbert improvement contribution remains bounded, not erased",
            "status": "COUNTERMODEL_CAUGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4600_decoupled_shadow_block",
            "input_branch": "decoupled conserved block or source-shadow/projector tail survives Hilbert extraction",
            "expected": "C_X^nonHilbert remains live through absolute envelope",
            "status": "COUNTERMODEL_CAUGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4600_no_cancellation",
            "input_branch": "boundary and non-Hilbert components have opposite signs in one fitted calibration",
            "expected": "absolute-sum envelope used unless parent signs cancellation",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4600_0_sources_exist",
            "claim": "all cited source paths exist",
            "passed": all(row["path_exists"] for row in sources),
            "detail": "source register path check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4600_1_needles_found",
            "claim": "all cited source needles found",
            "passed": all(row["needle_found"] for row in sources),
            "detail": "source register needle check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4600_2_boundary_nonHilbert_zero_or_bound",
            "claim": "boundary and non-Hilbert zero-or-bound theorem written",
            "passed": True,
            "detail": "same-branch zero route plus finite absolute fallback",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4600_3_final_CX_inserted",
            "claim": "C_X^final_live inserted into A_mem/A_h",
            "passed": True,
            "detail": "body-charge envelope no longer has an undifferentiated C_X live block",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4600_4_empirical_interface_ready",
            "claim": "next scoring inputs are named",
            "passed": True,
            "detail": "R10/PPN/clock/orbital/EM interface rows emitted but values missing",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4600_5_no_public_claim",
            "claim": "no local-GR/R10/PPN claim emitted",
            "passed": True,
            "detail": "parent signatures and numeric empirical rows remain missing",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "boundary_zero_or_norm": True,
            "nonHilbert_zero_or_norm": True,
            "final_CX_live_norm_inserted": True,
            "empirical_interface_ready": True,
            "parent_zero_or_numeric_bound_signed": False,
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "boundary zero-or-bound theorem; non-Hilbert/shadow zero-or-bound theorem; C_X^boundary_nonHilbert_live; C_X^final_live; A_mem/A_h final C update; empirical score interface",
            "not_derived": "parent-signed compact boundary silence; total non-Hilbert source-current zero; numeric C_X^final_live values; B_X/J_X/Q_boundary/Z_X/M_X^2 arena scoring; local-GR/R10/PPN pass",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The C_X matter-trace coupling ledger is now fully split; the useful next move is to assemble B_X, C_X, J_X, Q_boundary_X, Z_X and M_X^2 into arena score inputs.",
            "derive_first": "try to zero or source-own the full body-charge vector componentwise before numeric scoring",
            "fallback": "build nonclaim empirical score rows for R10/PPN/clock/orbital/EM with values missing rather than hiding placeholders",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4600 Y5 R2FR boundary/non-Hilbert zero or final C_X live norm

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4600 finishes the current `C_X` matter-trace coupling audit. The remaining 4599 block was:

```text
C_X^post4599 = C_X^std_weight_live + C_X^LHRS_live
             + C_X^boundary + C_X^nonHilbert.
```

The derivation attempt gives conditional zero routes:

```text
delta_X S_boundary=0 and Pi_local J_boundary_X=0
    => C_X^boundary=0,

P_source[J_NH]=0
    => C_X^nonHilbert=0.
```

Those clauses are not parent-signed in the live corpus, so 4600 does not claim local GR. It inserts the final explicit norm:

```text
C_X^boundary_nonHilbert_live = C_X^boundary + C_X^nonHilbert,

C_X^final_live = C_X^std_weight_live
               + C_X^LHRS_live
               + C_X^boundary_nonHilbert_live,

|C_X^final_live| <= |C_X^std_weight_live|
                  + |C_X^LHRS_live|
                  + |C_X^boundary|
                  + |C_X^nonHilbert|.
```

The key bookkeeping improvement is that `C_X` is no longer a fog bank. It is now a named vector of standard/weight, label-Hodge-support-readout, boundary and non-Hilbert/shadow pieces that can be theorem-zeroed or empirically scored component by component.

No R10, PPN, WEP, clock, orbital, EM or local-GR pass is claimed here.

## Source Register

{markdown_table(tables["sources"])}

## Boundary/Non-Hilbert Zero Theorem

{markdown_table(tables["zero"])}

## Final C_X Live Norm

{markdown_table(tables["norms"])}

## Body-Charge Envelope Update

{markdown_table(tables["body"])}

## Empirical Score Interface

{markdown_table(tables["interface"])}

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
    return f"""# PPC4161 616 - Boundary/Non-Hilbert Zero Or Final C_X Live Norm

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

For `X in {{mem,h}}`, define

```text
C_X^boundary_nonHilbert_live := C_X^boundary + C_X^nonHilbert
```

with conditional zeros

```text
delta_X S_boundary=0 and Pi_local J_boundary_X=0 => C_X^boundary=0,
P_source[J_NH]=0 => C_X^nonHilbert=0.
```

The live corpus does not parent-sign either total zero. Therefore the formal working coefficient is

```text
C_X^final_live = C_X^std_weight_live
               + C_X^LHRS_live
               + C_X^boundary_nonHilbert_live,

|C_X^final_live| <= |C_X^std_weight_live|
                  + |C_X^LHRS_live|
                  + |C_X^boundary|
                  + |C_X^nonHilbert|.
```

The memory/fibre body-charge envelopes use `C_mem^final_live` and `C_h^final_live`. Boundary Green charges `Q_boundary_X` remain separate and must not be hidden inside `C_X`.

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL4600_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    add("VAL4600_01_needles_found", all(row["needle_found"] for row in tables["sources"]), "all cited source needles found")
    csv_paths = [
        SOURCE_REGISTER,
        ZERO_THEOREM_CSV,
        FINAL_NORM_CSV,
        BODY_UPDATE_CSV,
        EMPIRICAL_INTERFACE_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    csv_ok = True
    details = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4600_02_csv_parse", csv_ok, ";".join(details))

    zero_text = "\n".join(str(row) for row in tables["zero"])
    add("VAL4600_03_zero_theorem_rows", "C_X^boundary=0" in zero_text and "C_X^nonHilbert=0" in zero_text, "boundary and non-Hilbert zero branches written")
    add("VAL4600_04_shadow_split", "C_shadow_pure_source_only=0" in zero_text and "C_readout_projector" in zero_text, "source-shadow split retained")

    norm_text = "\n".join(str(row) for row in tables["norms"])
    add("VAL4600_05_final_norm", "C_X^final_live" in norm_text and "epsilon_current_owner_NH_abs" in norm_text, "final C_X live norm rows written")

    body_text = "\n".join(str(row) for row in tables["body"])
    add("VAL4600_06_body_update", "C_mem^final_live" in body_text and "C_h^final_live" in body_text, "A_mem/A_h use final C_X")
    add("VAL4600_07_boundary_separation", "Q_boundary_X" in body_text and "separate" in body_text, "C boundary and Q boundary separated")

    interface_text = "\n".join(str(row) for row in tables["interface"])
    add("VAL4600_08_empirical_interface", all(token in interface_text for token in ["R10", "PPN", "clock", "orbital", "Poynting"]), "arena score interface rows written")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "local_GR_public_claim", "parent_zero_or_numeric_bound_signed"} and value is True:
                    all_false = False
    add("VAL4600_09_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4600_10_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4600_11_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4600_12_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4600_13_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4600_14_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4600_15_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4600_16_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4600_17_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4600_OVERALL", all(row["status"] == "PASS" for row in rows), "4600 boundary/non-Hilbert final C_X gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "zero": zero_theorem_rows(now),
        "norms": final_norm_rows(now),
        "body": body_update_rows(now),
        "interface": empirical_interface_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(ZERO_THEOREM_CSV, tables["zero"])
    write_csv(FINAL_NORM_CSV, tables["norms"])
    write_csv(BODY_UPDATE_CSV, tables["body"])
    write_csv(EMPIRICAL_INTERFACE_CSV, tables["interface"])
    write_csv(CONTROL_CSV, tables["controls"])
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
## PPC4161 Local Addendum - Boundary/Non-Hilbert Final C_X Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The `C_X` matter-trace coupling audit is now fully split. Boundary/reference leakage and non-Hilbert/shadow source-current leakage have conditional same-branch zero routes, but the live corpus does not parent-sign their total silence. The working object is therefore `C_X^final_live`, inserted into `A_mem/A_h` with `Q_boundary_X` kept as a separate Green-function boundary charge.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Final C_X Live Norm

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private local packet now has the final `C_X` live norm ready for empirical score assembly: standard/weight, label-Hodge-support-readout, boundary, and non-Hilbert/shadow pieces are explicit. The next packet step is the full body-charge vector `B_X,C_X,J_X,Q_boundary_X,Z_X,M_X^2`.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4600 validation failed: {failed}")
    print(f"4600 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
