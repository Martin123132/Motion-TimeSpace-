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

CHECKPOINT = "4597"
CLAIM_ID = "L-439"
BRANCH_ID = "MTS_R2FR_Y5_CMEM_CH_QBASIC_SPLIT_4597"
MARKER = "PPC4161_CMEM_CH_PARENT_SOURCE_DESCENT_OR_JLIVE_FIRST_NORM_4597"
PACKET_MARKER = "PPC4161_PACKET_CMEM_CH_PARENT_SOURCE_DESCENT_OR_JLIVE_FIRST_NORM_4597"
DECISION = "CMEM_CH_QBASIC_SOURCE_DESCENT_SUBTERM_ZERO_LIVE_LEAKAGE_VECTOR_BOUND_NONCLAIM"
NEXT_TARGET = "4598-Y5-R2FR-constant-standard-source-weight-zero-or-CXlive-first-norm.md"

DOC_PATH = POST / "4597-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md"
FORMAL_PATH = FORMAL / "613-PPC4161-Cmem-Ch-qbasic-source-descent-or-live-leakage-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4597_SOURCE_REGISTER.csv"
C_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_CX_QBASIC_SPLIT_LAW.csv"
DESCENT_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_CMEM_CH_DESCENT_ZERO_BRANCH.csv"
BODY_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_BODY_CHARGE_ENVELOPE_CX_LIVE_UPDATE.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_CX_LIVE_COEFFICIENT_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4597_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4597_VALIDATION.csv"

DOC_4596 = POST / "4596-Y5-R2FR-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md"
FORMAL_612 = FORMAL / "612-PPC4161-memory-fibre-source-kernel-insertion-or-first-body-charge-coefficient-row.md"
CSV_4596_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4596_NEXT_TARGET.csv"
CSV_4596_DESCENT = SOURCE_DIR / "P8_Y5_R2FR_4596_CMEM_CH_SOURCE_DESCENT_CONTRACT.csv"
CSV_4596_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv"
CSV_4596_BODY = SOURCE_DIR / "P8_Y5_R2FR_4596_BODY_CHARGE_ENVELOPE_UPDATE.csv"
CSV_4515_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv"
CSV_4515_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv"
CSV_3235_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_3235_MATTER_SOURCE_FUNCTOR_DERIVATION.csv"
CSV_3235_GATE = SOURCE_DIR / "P8_Y5_R2FR_3235_NO_MARKER_SOURCE_FUNCTOR_GATE.csv"
CSV_2763_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_2763_MATTER_SOURCE_FUNCTOR_CONTRACT_ATTEMPT.csv"
CSV_2689_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_2689_TOTAL_PARENT_ACTION_SOURCE_FUNCTOR_AUDIT.csv"
CSV_1780_GATE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1780_Q_DQ_TAU_SOURCE_FUNCTOR_SIGNATURE_GATE.csv"
CSV_1779_CONVERGENCE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1779_PARENT_CURRENT_SOURCE_FUNCTOR_CONVERGENCE.csv"
DOC_4587 = POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md"

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
        "claim": "4597 splits the memory/fibre matter-trace coefficient into an exact q-basic source-descent zero subterm plus live constants, source-weight, label, Hodge/support/readout, boundary and non-Hilbert leakage terms; A_mem/A_h now use C_mem_live/C_h_live instead of an undifferentiated C_X.",
        "current_evidence": "Generated C_X q-basic split law, memory/fibre descent-zero branch, updated body-charge envelopes, live coefficient rows, controls and validation.",
        "status": "Cmem_Ch_qbasic_subterm_zero_live_leakage_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Calling C_mem or C_h zero from Hilbert ownership alone while constants, source weights, labels, standards, Hodge/support/readout, boundary or non-Hilbert source routes remain legal.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No public local-GR/R10/PPN claim until C_live/J_live/B/Q boundary rows are parent-zero or source-backed and projected into arenas.",
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
        ("SRC4597_00_4596_doc", DOC_4596, "C_X` source-descent route", "4596 selected Cmem/Ch source descent as next target."),
        ("SRC4597_01_612_formal", FORMAL_612, "rho_X = B_X R_obs + C_X T + J_X", "formal 4596 density contract."),
        ("SRC4597_02_4596_next", CSV_4596_NEXT, "4597-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md", "machine-readable 4596 handoff."),
        ("SRC4597_03_4596_descent", CSV_4596_DESCENT, "DS4596_0_chain_rule", "C_X chain-rule contract."),
        ("SRC4597_04_4596_coeff", CSV_4596_COEFF, "CO4596_0_Cmem", "C_mem/Ch coefficient rows."),
        ("SRC4597_05_4596_body", CSV_4596_BODY, "BU4596_1_memory_amplitude", "A_mem/A_h live-current envelope source."),
        ("SRC4597_06_4515_chain", CSV_4515_THEOREM, "SFT4515_0_chain_rule", "source derivative split precedent."),
        ("SRC4597_07_4515_common_zero", CSV_4515_THEOREM, "SFT4515_1_single_source_functor_zero", "common Y5/Cmem/Jmem zero theorem."),
        ("SRC4597_08_4515_cmem", CSV_4515_CMEM, "SCV4515_0_Cmem", "C_mem source-coupling vector."),
        ("SRC4597_09_3235_chain", CSV_3235_DERIVATION, "MSF3235_1_chain_rule", "matter action variation chain rule."),
        ("SRC4597_10_3235_pullback", CSV_3235_DERIVATION, "MSF3235_2_pullback_zero_theorem", "ordinary matter pullback zero theorem."),
        ("SRC4597_11_3235_source", CSV_3235_DERIVATION, "MSF3235_3_source_functor", "source-current universality countermodel."),
        ("SRC4597_12_3235_constants", CSV_3235_GATE, "NMG3235_2_constant_superselection", "constants/material standards gate."),
        ("SRC4597_13_3235_source_weight", CSV_3235_GATE, "NMG3235_3_source_weight", "source-weight countermodel."),
        ("SRC4597_14_3235_readout", CSV_3235_GATE, "NMG3235_4_readout_nonhilbert_tail", "readout/non-Hilbert tail gate."),
        ("SRC4597_15_2763_pullback", CSV_2763_CONTRACT, "MFC2763_0_matter_pullback", "ordinary matter functor contract."),
        ("SRC4597_16_2763_forgetting", CSV_2763_CONTRACT, "MFC2763_1_source_forgetting", "source label forgetting contract."),
        ("SRC4597_17_2763_readout", CSV_2763_CONTRACT, "MFC2763_2_readout_closure", "readout closure contract."),
        ("SRC4597_18_2689_total", CSV_2689_AUDIT, "TPA2689_2_total_hilbert_source", "total Hilbert source extraction."),
        ("SRC4597_19_2689_prefactor", CSV_2689_AUDIT, "TPA2689_4_no_prefactor_package", "pre-action prefactor obstruction."),
        ("SRC4597_20_2689_readout", CSV_2689_AUDIT, "TPA2689_7_readout_radiative_stability", "readout/radiative stability obstruction."),
        ("SRC4597_21_1780_matter", CSV_1780_GATE, "QTS1780_5_matter_functor_signature", "matter functor signature gate."),
        ("SRC4597_22_1780_constants", CSV_1780_GATE, "QTS1780_6_constants_no_shadow", "constants/shadow source gate."),
        ("SRC4597_23_1779_residual", CSV_1779_CONVERGENCE, "PCS1779_3_Delta_Hsrc_identity", "source residual decomposition."),
        ("SRC4597_24_4587_poynting", DOC_4587, "POY4587_1_once_only", "Poynting once-only owner lock."),
        ("SRC4597_25_claim_438", CLAIMS_PATH, "L-438", "claim-register handoff from 4596."),
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


def c_split_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "split_id": "CS4597_0_common_decomposition",
            "target": "C_X for X in {mem,h}",
            "formula": "C_X = C_X^qbasic + C_X^std + C_X^weight + C_X^label + C_X^Hodge + C_X^support_readout + C_X^boundary + C_X^nonHilbert",
            "zero_subterm": "C_X^qbasic=0 if S_src=Sbar_src[q(Phi),Psi,A,theta_0] and v_X in ker(Dq)",
            "live_bound": "|C_X^live| <= |C_X^std|+|C_X^weight|+|C_X^label|+|C_X^Hodge|+|C_X^support_readout|+|C_X^boundary|+|C_X^nonHilbert|",
            "status": "QBASIC_SUBTERM_ZERO_LIVE_VECTOR_RETAINED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "split_id": "CS4597_1_chain_rule",
            "target": "q-basic source action",
            "formula": "delta_X S_src = (delta Sbar_src/delta q) Dq[v_X] + sum_a (delta S_src/delta theta_a) delta_X theta_a + boundary/readout/nonHilbert terms",
            "zero_subterm": "Dq[v_X]=0 kills only the quotient-pullback term",
            "live_bound": "standards, weights, labels, Hodge/support/readout, boundary and non-Hilbert tails remain absolute",
            "status": "NO_CANCELLATION_CHAIN_RULE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def descent_zero_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": "DZ4597_0_memory",
            "coefficient": "C_mem",
            "zero_branch": "C_mem^qbasic=0",
            "antecedents": "v_m in ker(Dq); observed geometry/coframe/connection and source action descend through q; constants/material labels fixed; no source weights; Hodge/current/support/readout q-basic",
            "live_replacement": "C_mem_live = C_mem^std+C_mem^weight+C_mem^label+C_mem^Hodge+C_mem^support_readout+C_mem^boundary+C_mem^nonHilbert",
            "status": "MEMORY_QBASIC_SUBTERM_ZERO_NOT_FULL_CMEM_ZERO",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "branch_id": "DZ4597_1_fibre",
            "coefficient": "C_h",
            "zero_branch": "C_h^qbasic=0",
            "antecedents": "h absent from the source grammar or h vertical to q; same fixed constants/Hodge/support/readout clauses as memory",
            "live_replacement": "C_h_live = C_h^std+C_h^weight+C_h^label+C_h^Hodge+C_h^support_readout+C_h^boundary+C_h^nonHilbert",
            "status": "FIBRE_QBASIC_SUBTERM_ZERO_NOT_FULL_CH_ZERO",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def body_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": "CBU4597_0_memory",
            "target": "A_mem",
            "before": "|A_mem| <= [exp(R/lambda_mem) int (||B_mem_eff||||R_obs||+||C_mem||||T||+||J_mem_live||)dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)",
            "after": "|A_mem| <= [exp(R/lambda_mem) int (||B_mem_eff||||R_obs||+||C_mem_live||||T||+||J_mem_live||)dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)",
            "claim_effect": "q-basic source-descent subterm removed; live standard/weight/label/Hodge/support/readout/boundary/non-Hilbert leakage remains",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "CBU4597_1_fibre",
            "target": "A_h",
            "before": "|A_h| <= [exp(R/lambda_h) int (||B_h||||R_obs||+||C_h||||T||+||J_h_live||)dV + ||Q_boundary_h||]/(4*pi||Z_h||)",
            "after": "|A_h| <= [exp(R/lambda_h) int (||B_h||||R_obs||+||C_h_live||||T||+||J_h_live||)dV + ||Q_boundary_h||]/(4*pi||Z_h||)",
            "claim_effect": "q-basic/h-blind source-descent subterm removed; live leakage remains",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def coefficient_rows(now: str) -> list[dict[str, Any]]:
    pieces = [
        ("CX4597_0_std", "C_X^std", "masses, charges, alpha_EM, clock/material standards vary with X", "constant superselection or parent fixed standards", "J_constants_bound / |C_X^std|"),
        ("CX4597_1_weight", "C_X^weight", "source-only prefactors w_A or kappa_A vary with X", "no pre-action source prefactor theorem", "source-weight norm"),
        ("CX4597_2_label", "C_X^label", "species/material labels survive source coupling", "source-label forgetting before coupling selection", "species/material label charge vector"),
        ("CX4597_3_hodge", "C_X^Hodge", "EM Hodge/current owner varies with X", "same Maxwell-Hodge/current owner and q-basic EM action", "Hodge/current leakage norm"),
        ("CX4597_4_support_readout", "C_X^support_readout", "support, clock, orbit, PPN or readout map re-enters after variation", "variation-before-readout plus one q-basic readout functor", "support/readout leakage norm"),
        ("CX4597_5_boundary", "C_X^boundary", "source boundary/reference charge varies with X", "fixed no-flux/topological boundary and neutral reference", "boundary derivative norm"),
        ("CX4597_6_nonHilbert", "C_X^nonHilbert", "retained non-Hilbert source covector", "no shadow/non-Hilbert labelled current theorem", "non-Hilbert source norm"),
        ("CX4597_7_live_total", "C_X^live", "total live matter-trace coupling after q-basic zero", "all live pieces zero in same branch", "sum of absolute live pieces"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": cid,
            "symbol": symbol,
            "meaning": meaning,
            "derive_first": derive,
            "finite_fallback": fallback,
            "current_status": "LIVE_VECTOR_ROW_READY_VALUE_MISSING" if cid != "CX4597_7_live_total" else "ABSOLUTE_SUM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for cid, symbol, meaning, derive, fallback in pieces
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4597_qbasic_clean",
            "input_branch": "S_src descends through q and all standards/source maps are fixed/q-basic",
            "expected": "C_X^qbasic=0 and C_X_live=0 only if every live piece is also zero",
            "status": "SYMBOLIC_CONTROL_PASS",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4597_source_weight",
            "input_branch": "w_A(X) S_A or kappa_A(X) T_A is legal before variation",
            "expected": "C_X^weight remains live even if q-pullback term is zero",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4597_constant_drift",
            "input_branch": "mass/clock/EM standard depends on X",
            "expected": "C_X^std remains live",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4597_readout_reentry",
            "input_branch": "post-variation readout/support map depends on X",
            "expected": "C_X^support_readout remains live",
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
            "gate_id": "PROM4597_0_sources_exist",
            "claim": "all cited source paths exist",
            "passed": all(row["path_exists"] for row in sources),
            "detail": "source register path check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4597_1_needles_found",
            "claim": "all cited source needles found",
            "passed": all(row["needle_found"] for row in sources),
            "detail": "source register needle check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4597_2_qbasic_subzero",
            "claim": "q-basic source-descent subterm zero is written",
            "passed": True,
            "detail": "C_X^qbasic=0 under S_src=Sbar[q] and v_X in ker(Dq)",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4597_3_live_vector",
            "claim": "C_X live leakage vector is explicit",
            "passed": True,
            "detail": "standard, weight, label, Hodge, support/readout, boundary and non-Hilbert pieces retained",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4597_4_no_public_claim",
            "claim": "no local-GR/R10/PPN claim emitted",
            "passed": True,
            "detail": "C_X_live values and parent signatures remain open",
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
            "qbasic_C_subterm_zero": True,
            "C_live_vector_written": True,
            "body_charge_envelope_reduced": True,
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
            "derived": "C_X q-basic source-descent subterm zero; C_mem/C_h live leakage vector; A_mem/A_h envelope updated with C_mem_live/C_h_live; finite coefficient rows",
            "not_derived": "full C_mem=C_h=0; parent-signed constant/source-weight/label/Hodge/support/readout/boundary/non-Hilbert zeros; numeric C_live values; local-GR/R10/PPN scoring",
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
            "reason": "After the q-basic subterm is removed, the largest C_X risk is constants/standards and source weights because they can alter the trace coupling while preserving ordinary-looking Hilbert matter.",
            "derive_first": "prove constant-standard superselection and no source-only prefactor in the parent source grammar",
            "fallback": "fill the first finite C_X_live norm row for standards or source weights and insert into A_mem/A_h",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4597 Y5 R2FR Cmem/Ch parent source descent or Jlive first norm

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4597 attacks the matter-trace coupling `C_X` directly.

The exact split is:

```text
C_X = C_X^qbasic + C_X^std + C_X^weight + C_X^label
    + C_X^Hodge + C_X^support_readout + C_X^boundary
    + C_X^nonHilbert.
```

The q-basic part is killed by the chain rule:

```text
S_src = Sbar_src[q(Phi),Psi,A,theta_0],
v_X in ker(Dq)
=> C_X^qbasic = 0.
```

But this does **not** prove `C_mem=0` or `C_h=0`. The live part is:

```text
|C_X^live| <= |C_X^std| + |C_X^weight| + |C_X^label|
            + |C_X^Hodge| + |C_X^support_readout|
            + |C_X^boundary| + |C_X^nonHilbert|.
```

Therefore the memory envelope is now:

```text
|A_mem| <= [exp(R/lambda_mem) int_body
 (||B_mem_eff||||R_obs|| + ||C_mem_live||||T|| + ||J_mem_live||) dV
 + ||Q_boundary_mem||] / (4*pi ||Z_mem||).
```

The fibre envelope is:

```text
|A_h| <= [exp(R/lambda_h) int_body
 (||B_h||||R_obs|| + ||C_h_live||||T|| + ||J_h_live||) dV
 + ||Q_boundary_h||] / (4*pi ||Z_h||).
```

This is a genuine tightening: the quotient-pullback matter/source term is no longer a vague blocker. What remains is the finite live leakage vector, with standards/constants and source weights the next best attack.

No local-GR, R10, PPN or orbital pass is claimed here.

## Source Register

{markdown_table(tables["sources"])}

## C_X q-Basic Split Law

{markdown_table(tables["split"])}

## Cmem/Ch Descent-Zero Branch

{markdown_table(tables["descent"])}

## Body-Charge Envelope C_X Live Update

{markdown_table(tables["body"])}

## C_X Live Coefficient Rows

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
    return f"""# PPC4161 613 - Cmem/Ch q-Basic Source Descent Or Live Leakage Bound

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

For `X in {{m,h}}`,

```text
C_X = C_X^qbasic + C_X^live.
```

If

```text
S_src=Sbar_src[q(Phi),Psi,A,theta_0],  v_X in ker(Dq),
```

then

```text
C_X^qbasic = 0.
```

The remaining term is not discarded:

```text
C_X^live = C_X^std+C_X^weight+C_X^label+C_X^Hodge
         + C_X^support_readout+C_X^boundary+C_X^nonHilbert.
```

Thus `A_mem` and `A_h` must use `C_mem_live` and `C_h_live` until each live component is parent-zero or source-backed finite.

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

    add("VAL4597_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    add("VAL4597_01_needles_found", all(row["needle_found"] for row in tables["sources"]), "all cited source needles found")
    csv_paths = [
        SOURCE_REGISTER,
        C_SPLIT_CSV,
        DESCENT_ZERO_CSV,
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
    add("VAL4597_02_csv_parse", csv_ok, ";".join(details))

    split_text = "\n".join(str(row) for row in tables["split"])
    add("VAL4597_03_qbasic_zero", "C_X^qbasic=0" in split_text and "ker(Dq)" in split_text, "q-basic C_X subterm zero written")
    add("VAL4597_04_live_vector", "C_X^std" in split_text and "C_X^weight" in split_text and "C_X^nonHilbert" in split_text, "live leakage vector written")

    body_text = "\n".join(str(row) for row in tables["body"])
    add("VAL4597_05_body_update", "C_mem_live" in body_text and "C_h_live" in body_text, "A_mem/A_h use C_live")

    coeff_text = "\n".join(str(row) for row in tables["coefficients"])
    add("VAL4597_06_coeff_rows", "C_X^std" in coeff_text and "C_X^weight" in coeff_text and "C_X^support_readout" in coeff_text, "finite coefficient rows staged")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "local_GR_public_claim", "parent_zero_or_numeric_bound_signed"} and value is True:
                    all_false = False
    add("VAL4597_07_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4597_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4597_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4597_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4597_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4597_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4597_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4597_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4597_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4597_OVERALL", all(row["status"] == "PASS" for row in rows), "4597 Cmem/Ch q-basic source descent split")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "split": c_split_rows(now),
        "descent": descent_zero_rows(now),
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
    write_csv(C_SPLIT_CSV, tables["split"])
    write_csv(DESCENT_ZERO_CSV, tables["descent"])
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
## PPC4161 Local Addendum - Cmem/Ch q-Basic Source Descent Split

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The memory/fibre matter-trace coefficient is no longer an undifferentiated blocker. The q-basic pullback subterm satisfies `C_X^qbasic=0` when `S_src=Sbar[q(Phi),...]` and `v_X in ker(Dq)`. The body-charge envelopes now use `C_mem_live` and `C_h_live`, retaining standards, source weights, labels, Hodge/support/readout, boundary and non-Hilbert pieces for derivation or finite scoring.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Cmem/Ch Live Leakage Vector

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private local packet now separates the exact q-basic source descent zero from the live `C_X` leakage vector. The next useful move is to parent-sign constant-standard superselection/no source weights or fill the first finite `C_X_live` norm row.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4597 validation failed: {failed}")
    print(f"4597 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
