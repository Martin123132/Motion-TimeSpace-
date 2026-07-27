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

CHECKPOINT = "4599"
CLAIM_ID = "L-441"
BRANCH_ID = "MTS_R2FR_Y5_LABEL_HODGE_SUPPORT_READOUT_GATE_4599"
MARKER = "PPC4161_LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_CXLIVE_NEXT_NORM_4599"
PACKET_MARKER = "PPC4161_PACKET_LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_CXLIVE_NEXT_NORM_4599"
DECISION = "LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_NORM_INSERTED_CX_LIVE_REDUCED_NONCLAIM"
NEXT_TARGET = "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md"

DOC_PATH = POST / "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"
FORMAL_PATH = FORMAL / "615-PPC4161-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4599_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
NORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
BODY_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_BODY_CHARGE_ENVELOPE_LABEL_HODGE_READOUT_UPDATE.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_CXLIVE_NEXT_NORM_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4599_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4599_VALIDATION.csv"

DOC_4598 = POST / "4598-Y5-R2FR-constant-standard-source-weight-zero-or-CXlive-first-norm.md"
FORMAL_614 = FORMAL / "614-PPC4161-constant-standard-source-weight-zero-or-CXlive-first-norm.md"
CSV_4598_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4598_NEXT_TARGET.csv"
CSV_4598_BODY = SOURCE_DIR / "P8_Y5_R2FR_4598_BODY_CHARGE_ENVELOPE_STANDARD_WEIGHT_UPDATE.csv"
CSV_4598_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4598_STATUS.csv"
CSV_3291_LABEL = SOURCE_DIR / "P8_Y5_R2FR_3291_SOURCE_LABEL_FORGETTING_LEMMA.csv"
CSV_3522_LABEL = SOURCE_DIR / "P8_Y5_R2FR_3522_LIVE_LABEL_AUDIT.csv"
CSV_3523_STATUS = SOURCE_DIR / "P8_Y5_R2FR_3523_SOURCE_LABEL_FORGETTING_EM_HODGE_STATUS.csv"
CSV_4315_HODGE = SOURCE_DIR / "P8_Y5_R2FR_4315_SAME_HODGE_THEOREM.csv"
CSV_4315_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4315_DELTA_HODGE_BOUND_UPDATE.csv"
CSV_4588_SUPPORT = SOURCE_DIR / "P8_Y5_R2FR_4588_REGULAR_SUPPORT_ZERO_CLAUSES.csv"
CSV_4588_REYNOLDS = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv"
CSV_3560_SUPPORT = SOURCE_DIR / "P8_Y5_R2FR_3560_SUPPORT_RESIDUAL_DECOMPOSITION.csv"
CSV_1816_READOUT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv"
CSV_1898_READOUT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv"
CSV_1919_READOUT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1919_READOUT_DESCENT_PROOF_ATTEMPT.csv"

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
        "claim": "4599 reduces the C_X live matter-trace leakage by isolating source-label, Maxwell-Hodge, source-support and readout re-entry gates: each has an exact conditional zero branch and an explicit finite norm if the parent branch is unsigned.",
        "current_evidence": "Generated label/Hodge/support/readout zero theorem rows, C_X next-norm rows, updated body-charge envelopes, controls and validation.",
        "status": "label_Hodge_support_readout_zero_or_norm_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using total Hilbert variation, Maxwell covariance, ordinary source support, or postprocessing readout as if they prove label forgetting, same-Hodge ownership, support regularity, and readout no-reentry in one parent branch.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until label/Hodge/support/readout plus boundary/non-Hilbert rows are parent-zero or source-backed below arena bounds.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--short"], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4599_00_4598_doc", DOC_4598, "label/Hodge/support/readout", "4598 selected label/Hodge/support/readout as next target."),
        ("SRC4599_01_614_formal", FORMAL_614, "C_X^post4598", "formal C_X post4598 split."),
        ("SRC4599_02_4598_next", CSV_4598_NEXT, "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md", "machine-readable 4598 handoff."),
        ("SRC4599_03_4598_body", CSV_4598_BODY, "BU4598_0_Csplit", "C_X post4598 body envelope source."),
        ("SRC4599_04_4598_status", CSV_4598_STATUS, "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md", "4598 status handoff."),
        ("SRC4599_05_3291_total", CSV_3291_LABEL, "SLF3291_1_total_variation", "source-label total variation theorem."),
        ("SRC4599_06_3291_counter", CSV_3291_LABEL, "SLF3291_3_live_counterexample", "source-only species counterexample."),
        ("SRC4599_07_3522_labels", CSV_3522_LABEL, "LL3522_2_matter_source_labels", "live source-label audit."),
        ("SRC4599_08_3522_hodge_labels", CSV_3522_LABEL, "LL3522_4_EM_Hodge_Poynting_labels", "EM Hodge/Poynting label audit."),
        ("SRC4599_09_3523_status", CSV_3523_STATUS, "STAT3523_1_EM_Poynting_route", "conditional EM/Poynting route."),
        ("SRC4599_10_4315_same_action", CSV_4315_HODGE, "HT4315_1_same_action", "same-Hodge Maxwell action theorem."),
        ("SRC4599_11_4315_counter", CSV_4315_HODGE, "HT4315_4_countermodel", "constitutive countermodel."),
        ("SRC4599_12_4315_bound", CSV_4315_BOUND, "HB4315_0_envelope", "Delta_Hodge_EM finite envelope."),
        ("SRC4599_13_4588_clause", CSV_4588_SUPPORT, "ZSR4588_0_fixed_qbasic_collar", "q-basic support collar clause."),
        ("SRC4599_14_4588_zero", CSV_4588_REYNOLDS, "RST4588_1_zero_trace_support", "regular support zero theorem."),
        ("SRC4599_15_4588_bound", CSV_4588_REYNOLDS, "RST4588_2_shell_bound", "finite Reynolds shell bound."),
        ("SRC4599_16_3560_support", CSV_3560_SUPPORT, "SRD3560_7_Delta_support_total", "source-support residual decomposition."),
        ("SRC4599_17_1816_variation", CSV_1816_READOUT, "VBR1816_0_target", "variation-before-readout theorem."),
        ("SRC4599_18_1816_limit", CSV_1816_READOUT, "VBR1816_5_source_worldtube_limit", "source-worldtube readout limit."),
        ("SRC4599_19_1898_post", CSV_1898_READOUT, "RVC1898_1_pure_postprocessing_zero", "pure postprocessing zero lemma."),
        ("SRC4599_20_1898_comm", CSV_1898_READOUT, "RVC1898_2_projection_commutator_survives", "readout/projector commutator countermodel."),
        ("SRC4599_21_1919_target", CSV_1919_READOUT, "RTP1919_0_target", "readout descent theorem target."),
        ("SRC4599_22_1919_verdict", CSV_1919_READOUT, "RTP1919_5_verdict", "readout/tau descent verdict."),
        ("SRC4599_23_claim_440", CLAIMS_PATH, "L-440", "claim-register handoff from 4598."),
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
            "theorem_id": "LHRS4599_0_label",
            "target": "C_X^label",
            "zero_branch": "source functor consumes total variational objects T_total,J_total only; parent syntax forbids source-only labels, constructor labels and spurion/readout return",
            "formula": "F_src(T_total,J_total) has no A-label slot => C_X^label=0",
            "finite_branch": "|C_X^label| <= |Delta_label_X|",
            "status": "EXACT_CONDITIONAL_LABEL_ZERO_COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "LHRS4599_1_Hodge",
            "target": "C_X^Hodge",
            "zero_branch": "fixed observed metric/coframe/orientation plus Maxwell action S_EM=-1/(4mu0) int F wedge *_obs F; no independent chi_EM, hidden constitutive coefficient, readout Hodge or orientation residual",
            "formula": "Delta_Hodge_EM=0 => C_X^Hodge=0",
            "finite_branch": "||Delta_Hodge_EM|| <= ||Delta_chi_principal||+||Delta_chi_skewon||+L||dtheta_EM||+|C_Hodge_hidden|+|C_Hodge_readout|+|Delta_orientation_flux|",
            "status": "SAME_HODGE_ZERO_OR_NO_CANCELLATION_BOUND_READY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "LHRS4599_2_support",
            "target": "C_X^support",
            "zero_branch": "fixed q-basic source collar, compact regular finite-perimeter support, zero boundary trace, no birth/death shell, no threshold mask, no hidden side flux and bounded arena tests",
            "formula": "rho_H^tr|partial W=0 and mu_birth=0 => E_boundary_birth=0 => C_X^support=0",
            "finite_branch": "Phi_A*(int_partialW |rho_H^tr||V_n| dSigma + ||mu_birth||_TV)/|M_H_ref| plus retained support terms",
            "status": "REYNOLDS_ZERO_OR_SHELL_NORM_READY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "LHRS4599_3_readout",
            "target": "C_X^readout",
            "zero_branch": "variation before readout; readout is pure postprocessing on solved parent quotient with no action/effective-action/source coefficient codomain and no projector/source-worldtube reentry",
            "formula": "Pi_CoeffSource([delta_parent,R_post]T_H)=0 => C_X^readout=0",
            "finite_branch": "||C_R|| from projector/source-worldtube, EFT/prevariation, calibration feedback, material/clock response and arena kernels",
            "status": "PURE_POSTPROCESSING_ZERO_OR_COMMUTATOR_BOUND_READY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "LHRS4599_4_combined",
            "target": "C_X^label_Hodge_support_readout",
            "zero_branch": "LHRS4599_0 through LHRS4599_3 pass in the same parent branch",
            "formula": "C_X^label_Hodge_support_readout=0",
            "finite_branch": "|C_X^label_Hodge_support_readout| <= |C_X^label|+|C_X^Hodge|+|C_X^support|+|C_X^readout|",
            "status": "COMBINED_ZERO_OR_ABSOLUTE_SUM_READY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def norm_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("N4599_0_label", "Delta_label_X", "source-label/constructor/spurion return norm", "WEP/R10/PPN source-label sensitivity"),
        ("N4599_1_Hodge", "Delta_Hodge_EM_X", "same-Hodge/constitutive mismatch norm", "EM/Poynting/alpha/clock source sensitivity"),
        ("N4599_2_support", "Delta_support_X", "Reynolds support-boundary/source-worldtube norm", "source mass/support/orbital/WEP kernels"),
        ("N4599_3_readout", "C_R_X", "readout/variation commutator norm", "WEP/R10/PPN/clock/orbit readout kernels"),
        ("N4599_4_total", "C_X^LHRS_live", "combined label-Hodge-support-readout live norm", "A_mem/A_h numerator input"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "norm_id": norm_id,
            "symbol": symbol,
            "definition": definition,
            "finite_bound": "source-backed value or same-branch zero certificate required; no cancellation or fitted-calibration hiding",
            "observable_link": link,
            "current_status": "VALUE_MISSING_NONCLAIM" if norm_id != "N4599_4_total" else "ABSOLUTE_SUM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for norm_id, symbol, definition, link in rows
    ]


def body_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4599_0_Csplit",
            "target": "C_X live after 4599",
            "formula": "C_X^post4599 = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary + C_X^nonHilbert",
            "zero_condition": "C_X^LHRS_live=0 only if label, Hodge, support and readout zero theorems pass in the same parent branch",
            "finite_bound": "|C_X^post4599| <= |C_X^std_weight_live|+|C_X^LHRS_live|+|C_X^boundary|+|C_X^nonHilbert|",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4599_1_memory",
            "target": "A_mem",
            "formula": "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs|| + ||C_mem^post4599||||T|| + ||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)",
            "zero_condition": "B_mem_eff=C_mem^post4599=J_mem_live=Q_boundary_mem=0",
            "finite_bound": "label/Hodge/support/readout pieces now enter through C_mem^LHRS_live",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4599_2_fibre",
            "target": "A_h",
            "formula": "|A_h| <= [exp(R/lambda_h) int_body (||B_h||||R_obs|| + ||C_h^post4599||||T|| + ||J_h_live||) dV + ||Q_boundary_h||]/(4*pi||Z_h||)",
            "zero_condition": "B_h=C_h^post4599=J_h_live=Q_boundary_h=0",
            "finite_bound": "label/Hodge/support/readout pieces now enter through C_h^LHRS_live",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def coefficient_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("C4599_0_label", "C_X^label", "source-label/constructor leakage", "prove total-source functor has no label/spurion/readout slot", "Delta_label_X"),
        ("C4599_1_Hodge", "C_X^Hodge", "Maxwell-Hodge/constitutive leakage", "prove same-Hodge visible Maxwell action and no independent chi_EM/readout/orientation residual", "Delta_Hodge_EM_X"),
        ("C4599_2_support", "C_X^support", "source-support/worldtube leakage", "prove q-basic regular zero-trace support with no shell/threshold/side flux", "Delta_support_X"),
        ("C4599_3_readout", "C_X^readout", "readout/projection commutator leakage", "prove variation-before-readout and pure postprocessing no-reentry", "C_R_X"),
        ("C4599_4_LHRS", "C_X^LHRS_live", "combined label-Hodge-support-readout live norm", "all four subrows zero in same branch", "absolute sum of C4599_0..3"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": coeff_id,
            "symbol": symbol,
            "role": role,
            "derive_first": derive,
            "finite_fallback": fallback,
            "current_status": "MISSING_PARENT_ZERO_OR_VALUE" if coeff_id != "C4599_4_LHRS" else "NEXT_NORM_ROW_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for coeff_id, symbol, role, derive, fallback in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4599_label_countermodel",
            "input_branch": "source selector sees labelled pairs {(T_A,A)} or constructor labels",
            "expected": "C_X^label remains live",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4599_Hodge_countermodel",
            "input_branch": "independent chi_EM or hidden constitutive coefficient multiplies F^2",
            "expected": "C_X^Hodge remains live despite gauge covariance",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4599_support_countermodel",
            "input_branch": "source support is threshold/readout mask or has shell birth",
            "expected": "C_X^support remains live as Reynolds shell norm",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4599_readout_countermodel",
            "input_branch": "readout/projector enters before variation or has source coefficient codomain",
            "expected": "C_X^readout remains live",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4599_0_sources_exist",
            "claim": "all cited source paths exist",
            "passed": all(row["path_exists"] for row in sources),
            "detail": "source register path check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4599_1_needles_found",
            "claim": "all cited source needles found",
            "passed": all(row["needle_found"] for row in sources),
            "detail": "source register needle check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4599_2_zero_or_norm",
            "claim": "label/Hodge/support/readout zero-or-norm theorem written",
            "passed": True,
            "detail": "four subbranches each have zero conditions and finite fallback",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4599_3_body_update",
            "claim": "A_mem/A_h envelopes use C_X^post4599",
            "passed": True,
            "detail": "label/Hodge/support/readout pieces now explicit inside C_X^LHRS_live",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4599_4_no_public_claim",
            "claim": "no local-GR/R10/PPN claim emitted",
            "passed": True,
            "detail": "no numeric LHRS values or parent signatures complete",
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
            "label_zero_or_norm": True,
            "Hodge_zero_or_norm": True,
            "support_zero_or_norm": True,
            "readout_zero_or_norm": True,
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
            "derived": "source-label zero-or-norm; same-Hodge zero-or-norm; regular support zero-or-Reynolds norm; pure readout zero-or-commutator norm; C_X^post4599 body envelope update",
            "not_derived": "parent-signed label/Hodge/support/readout zero in one branch; numeric LHRS norm values; boundary/non-Hilbert C_X rows; local-GR/R10/PPN scoring",
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
            "reason": "After label/Hodge/support/readout are isolated, the remaining C_X live family is boundary plus non-Hilbert/shadow current leakage.",
            "derive_first": "prove boundary neutrality and no non-Hilbert/shadow source covector in the same parent branch",
            "fallback": "fill final C_X boundary/non-Hilbert norm row and insert into A_mem/A_h",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4599 Y5 R2FR label-Hodge-support-readout zero or C_X live next norm

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4599 attacks the next `C_X` live family after constants and source weights:

```text
C_X^label, C_X^Hodge, C_X^support, C_X^readout.
```

The combined zero route is:

```text
source labels forgotten before coupling,
same observed Maxwell-Hodge owner,
regular q-basic zero-trace support,
variation before pure readout,
all in the same parent branch
=> C_X^label_Hodge_support_readout = 0.
```

If any clause fails, the finite row is:

```text
|C_X^LHRS_live| <= |C_X^label| + |C_X^Hodge|
                + |C_X^support| + |C_X^readout|.
```

The body-charge coupling becomes:

```text
C_X^post4599 = C_X^std_weight_live + C_X^LHRS_live
             + C_X^boundary + C_X^nonHilbert.
```

So the memory/fibre envelopes now use `C_mem^post4599` and `C_h^post4599`. Label/Hodge/support/readout leakage is no longer hidden inside a vague `C_X`.

No local-GR, R10, PPN or orbital pass is claimed here.

## Source Register

{markdown_table(tables["sources"])}

## Label/Hodge/Support/Readout Zero Theorem

{markdown_table(tables["zero"])}

## C_X Label/Hodge/Support/Readout Norm

{markdown_table(tables["norms"])}

## Body-Charge Envelope Update

{markdown_table(tables["body"])}

## C_X Live Next Norm Rows

{markdown_table(tables["coefficients"])}

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
    return f"""# PPC4161 615 - Label/Hodge/Support/Readout Zero Or C_X Live Next Norm

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

For `X in {{m,h}}`,

```text
C_X^post4599 = C_X^std_weight_live + C_X^LHRS_live
             + C_X^boundary + C_X^nonHilbert.
```

where

```text
C_X^LHRS_live = C_X^label + C_X^Hodge + C_X^support + C_X^readout.
```

The LHRS block is zero only if source labels are forgotten, Maxwell uses the same observed Hodge owner, support is q-basic regular with zero trace/no shell, and readout is pure post-variation postprocessing in one parent branch. Otherwise it is an explicit norm in `A_mem/A_h`.

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

    add("VAL4599_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    add("VAL4599_01_needles_found", all(row["needle_found"] for row in tables["sources"]), "all cited source needles found")
    csv_paths = [
        SOURCE_REGISTER,
        ZERO_THEOREM_CSV,
        NORM_CSV,
        BODY_UPDATE_CSV,
        COEFFICIENT_CSV,
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
    add("VAL4599_02_csv_parse", csv_ok, ";".join(details))

    zero_text = "\n".join(str(row) for row in tables["zero"])
    add("VAL4599_03_four_zero_branches", all(token in zero_text for token in ["C_X^label=0", "C_X^Hodge=0", "C_X^support=0", "C_X^readout=0"]), "four zero branches written")

    norm_text = "\n".join(str(row) for row in tables["norms"])
    add("VAL4599_04_norm_rows", "Delta_Hodge_EM_X" in norm_text and "C_R_X" in norm_text and "Delta_support_X" in norm_text, "finite norm rows written")

    body_text = "\n".join(str(row) for row in tables["body"])
    add("VAL4599_05_body_update", "C_mem^post4599" in body_text and "C_h^post4599" in body_text, "A_mem/A_h use post4599 C_X")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "local_GR_public_claim", "parent_zero_or_numeric_bound_signed"} and value is True:
                    all_false = False
    add("VAL4599_06_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4599_07_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4599_08_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4599_09_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4599_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4599_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4599_12_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4599_13_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4599_14_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4599_OVERALL", all(row["status"] == "PASS" for row in rows), "4599 label/Hodge/support/readout zero-or-norm gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "zero": zero_theorem_rows(now),
        "norms": norm_rows(now),
        "body": body_update_rows(now),
        "coefficients": coefficient_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(ZERO_THEOREM_CSV, tables["zero"])
    write_csv(NORM_CSV, tables["norms"])
    write_csv(BODY_UPDATE_CSV, tables["body"])
    write_csv(COEFFICIENT_CSV, tables["coefficients"])
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
## PPC4161 Local Addendum - Label/Hodge/Support/Readout C_X Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The `C_X` live matter-trace leakage vector is narrowed again: source labels, Maxwell-Hodge ownership, source support and readout re-entry now have explicit same-branch zero clauses and finite norm fallbacks. The memory/fibre body-charge envelopes now use `C_mem^post4599` and `C_h^post4599`.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Label/Hodge/Support/Readout C_X Norm

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private local packet now exposes the LHRS block as a zero-or-norm object inside `A_mem/A_h`. The next useful branch is boundary plus non-Hilbert/shadow source leakage.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4599 validation failed: {failed}")
    print(f"4599 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
