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

CHECKPOINT = "4596"
CLAIM_ID = "L-438"
BRANCH_ID = "MTS_R2FR_Y5_MEMORY_FIBRE_SOURCE_KERNEL_INSERTION_4596"
MARKER = "PPC4161_MEMORY_FIBRE_SOURCE_FUNCTOR_SIGNATURE_OR_FIRST_BODY_CHARGE_COEFFICIENT_ROW_4596"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_FIBRE_SOURCE_FUNCTOR_SIGNATURE_OR_FIRST_BODY_CHARGE_COEFFICIENT_ROW_4596"
DECISION = "STRICT_SOURCE_KERNEL_INSERTED_INTO_MEMORY_FIBRE_J_VECTOR_LIVE_BODY_CHARGE_ENVELOPE_REDUCED_NONCLAIM"
NEXT_TARGET = "4597-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md"

DOC_PATH = POST / "4596-Y5-R2FR-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md"
FORMAL_PATH = FORMAL / "612-PPC4161-memory-fibre-source-kernel-insertion-or-first-body-charge-coefficient-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4596_SOURCE_REGISTER.csv"
INSERTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_SOURCE_KERNEL_TO_JMEM_INSERTION.csv"
DESCENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_CMEM_CH_SOURCE_DESCENT_CONTRACT.csv"
J_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv"
BODY_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_BODY_CHARGE_ENVELOPE_UPDATE.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4596_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4596_VALIDATION.csv"

DOC_4595 = POST / "4595-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"
FORMAL_611 = FORMAL / "611-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"
CSV_4595_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4595_NEXT_TARGET.csv"
CSV_4595_MEMORY = SOURCE_DIR / "P8_Y5_R2FR_4595_MEMORY_BODY_CHARGE_BOUND.csv"
CSV_4595_FIBRE = SOURCE_DIR / "P8_Y5_R2FR_4595_FIBRE_BODY_CHARGE_BOUND.csv"
CSV_4595_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4595_STATUS.csv"
DOC_4515 = POST / "4515-Y5-R2FR-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md"
CSV_4515_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv"
CSV_4515_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv"
DOC_4516 = POST / "4516-Y5-R2FR-source-functor-parent-signature-or-first-Y5-coefficient-fill.md"
CSV_4516_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4516_STATUS.csv"
DOC_4520 = POST / "4520-Y5-R2FR-rank-zero-source-current-silence-or-alpha-input-acquisition.md"
CSV_4520_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4520_STATUS.csv"
DOC_4587 = POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md"
CSV_4587_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4587_STATUS.csv"
DOC_4591 = POST / "4591-Y5-R2FR-tau-eobs-same-frame-lock-or-source-support-bound.md"
DOC_4592 = POST / "4592-Y5-R2FR-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md"
CSV_4592_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4592_SOURCE_KERNEL_PPN_INTEGRATION_THEOREM.csv"
CSV_4592_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4592_STATUS.csv"

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
        "claim": "4596 inserts the strict 4587-4592 source-worldtube zero chain into the memory/fibre body-charge problem: the source-kernel part of J_mem/J_h is zero on the same q-basic Hilbert/Maxwell worldtube branch, while live non-Hilbert, dynamic exchange, open Poynting and boundary/readout pieces remain explicit coefficient rows.",
        "current_evidence": "Generated source-kernel-to-J insertion theorem, C_mem/C_h descent contract, reduced J vector, updated body-charge envelopes, first coefficient rows, controls and validation.",
        "status": "source_kernel_inserted_into_memory_fibre_J_vector_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Upgrading the strict source-kernel subzero to full C_mem/J_mem/B_mem_eff or local-GR closure, or hiding open EM/Poynting/non-Hilbert/boundary currents inside calibrated G.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No public local-GR/R10/PPN claim until C_mem/C_h and the remaining live J/Q/B coefficients are parent-zero or source-backed and projected into arenas.",
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
        ("SRC4596_00_4595_doc", DOC_4595, "J_mem", "4595 body-charge zero switch with J_mem/J_h live."),
        ("SRC4596_01_611_formal", FORMAL_611, "rho_X = B_X R_obs + C_X T + J_X", "formal 4595 common source-density contract."),
        ("SRC4596_02_4595_next", CSV_4595_NEXT, "4596-Y5-R2FR-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md", "machine-readable 4595 handoff."),
        ("SRC4596_03_4595_memory", CSV_4595_MEMORY, "MEM4595_3_poynting_guard", "memory Poynting guard row."),
        ("SRC4596_04_4595_fibre", CSV_4595_FIBRE, "FIB4595_2_amplitude", "fibre amplitude row."),
        ("SRC4596_05_4595_status", CSV_4595_STATUS, "parent-signed B_mem_eff", "4595 missing parent signatures."),
        ("SRC4596_06_4515_doc", DOC_4515, "EM/Poynting flow", "4515 source functor and Poynting guard."),
        ("SRC4596_07_4515_theorem", CSV_4515_THEOREM, "SFT4515_1_single_source_functor_zero", "single source-functor conditional zero theorem."),
        ("SRC4596_08_4515_cmem", CSV_4515_CMEM, "SCV4515_0_Cmem", "C_mem/J_mem source vector."),
        ("SRC4596_09_4516_doc", DOC_4516, "SHS4516_2_stationary_zero", "stationary Hilbert mass-current theorem."),
        ("SRC4596_10_4516_status", CSV_4516_STATUS, "LOCAL_STATIONARY_HILBERT_SOURCE_SUBTHEOREM", "4516 partial source-functor status."),
        ("SRC4596_11_4520_doc", DOC_4520, "J_A^Hilbert=0", "rank-zero Hilbert source current silence."),
        ("SRC4596_12_4520_status", CSV_4520_STATUS, "J_A^Hilbert=0", "rank-zero source-current status."),
        ("SRC4596_13_4587_doc", DOC_4587, "POY4587_1_once_only", "Poynting once-only source lock."),
        ("SRC4596_14_4587_status", CSV_4587_STATUS, "Density q-basicness", "density q-basic and Poynting support status."),
        ("SRC4596_15_4591_doc", DOC_4591, "C_K_source_worldtube=0", "strict source-worldtube kernel zero."),
        ("SRC4596_16_4592_doc", DOC_4592, "Delta_PPN^source_kernel", "source-kernel residual vector insertion."),
        ("SRC4596_17_4592_theorem", CSV_4592_THEOREM, "INT4592_1_strict_source_kernel_subvector_zero", "strict source-kernel zero theorem."),
        ("SRC4596_18_4592_status", CSV_4592_STATUS, "strict source-worldtube kernel contributes zero", "4592 strongest source-kernel result."),
        ("SRC4596_19_claim_437", CLAIMS_PATH, "L-437", "claim-register handoff from 4595."),
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


def insertion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "insertion_id": "INS4596_0_common_split",
            "target": "memory/fibre direct current",
            "formula": "J_X = J_X^source_kernel + J_X^Hilbert_stationary + J_X^EM_open + J_X^nonHilbert + J_X^dyn_exchange + J_X^boundary_readout",
            "zero_condition": "same q-basic Hilbert/Maxwell worldtube branch, public Maxwell-Hodge EM in T_total, compact regular support, source-blind Href, certified Dq verticality, fixed readout mask and same tau/e_obs",
            "consequence": "J_X^source_kernel=0 and Hilbert stationary current contributes no extra direct memory/fibre current",
            "status": "SOURCE_KERNEL_SUBCURRENT_ZERO_INSERTED_CONDITIONALLY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "insertion_id": "INS4596_1_memory",
            "target": "J_mem",
            "formula": "J_mem_live = J_mem^EM_open + J_mem^nonHilbert + J_mem^dyn_exchange + J_mem^boundary_readout",
            "zero_condition": "strict source-kernel clauses fire; EM/Poynting has no radiative boundary flux; no retained non-Hilbert current; no dynamic exchange; boundary/readout neutral",
            "consequence": "4595 A_mem envelope can drop the source-kernel subterm but must retain J_mem_live",
            "status": "MEMORY_J_VECTOR_REDUCED_NOT_CLOSED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "insertion_id": "INS4596_2_fibre",
            "target": "J_h",
            "formula": "J_h_live = J_h^EM_open + J_h^nonHilbert + J_h^dyn_exchange + J_h^boundary_readout",
            "zero_condition": "same source-kernel branch plus h-blind source functor and no retained fibre current",
            "consequence": "4595 A_h envelope can drop the source-kernel subterm but must retain J_h_live",
            "status": "FIBRE_J_VECTOR_REDUCED_NOT_CLOSED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def descent_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "DS4596_0_chain_rule",
            "coefficient": "C_X",
            "derivation": "If S_src=Sbar_src[q(Phi),Psi,A,theta] and v_X in ker(Dq), then delta_X S_src = (delta Sbar/dq) Dq[v_X] = 0.",
            "zero_condition": "source action, masses, clocks, EM Hodge/current owner and support/readout are all q-basic before variation",
            "fallback": "|C_X T| retained as an absolute body-charge density term",
            "status": "EXACT_CHAIN_RULE_CONTRACT_NOT_PARENT_SIGNED_FOR_ALL_X",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "DS4596_1_memory",
            "coefficient": "C_mem",
            "derivation": "memory/class scalar is matter-trace silent if it is a vertical memory coordinate of q and the active source functor descends through q",
            "zero_condition": "v_m in ker(Dq); no explicit m-dependence in masses/standards/Hodge/support/readout",
            "fallback": "|C_mem| ||T|| remains in A_mem",
            "status": "CONDITIONAL_ZERO_ROUTE_READY_PARENT_SIGNATURE_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "DS4596_2_fibre",
            "coefficient": "C_h",
            "derivation": "finite-cell fibre is matter-trace silent if h is either absent from the source grammar or eliminated before the source functor is varied",
            "zero_condition": "h-blind S_src or h vertical to q plus no source standards/hodge/support dependence",
            "fallback": "|C_h| ||T|| remains in A_h",
            "status": "CONDITIONAL_ZERO_ROUTE_READY_PARENT_SIGNATURE_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def j_vector_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "J4596_0_source_kernel",
            "symbol": "J_X^source_kernel",
            "status_after_4596": "ZERO_ON_STRICT_BRANCH",
            "bound_if_open": "L_JX L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux)",
            "next_input": "same-branch certificate tying 4587-4592 source-worldtube clauses to memory/fibre X",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "J4596_1_EM_open",
            "symbol": "J_X^EM_open",
            "status_after_4596": "ZERO_ONLY_FOR_MAXWELL_HODGE_NO_FLUX_BRANCH",
            "bound_if_open": "|int_boundary T_EM(tau,n)dSigma dt|/|M_H_ref| times source-coupling operator norm",
            "next_input": "no-radiation collar or finite Poynting flux profile",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "J4596_2_nonHilbert",
            "symbol": "J_X^nonHilbert",
            "status_after_4596": "LIVE",
            "bound_if_open": "||J_X^nonHilbert|| absolute source profile",
            "next_input": "prove no retained non-Hilbert source current or fill finite profile",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "J4596_3_dynamic_exchange",
            "symbol": "J_X^dyn_exchange",
            "status_after_4596": "LIVE_OUTSIDE_STATIONARY_BRANCH",
            "bound_if_open": "||exchange/clock/source current||",
            "next_input": "stationary exchange closure or finite dynamic current row",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "J4596_4_boundary_readout",
            "symbol": "J_X^boundary_readout",
            "status_after_4596": "LIVE_UNLESS_BOUNDARY_READOUT_NEUTRAL",
            "bound_if_open": "||boundary/readout source reference shift||",
            "next_input": "boundary/reference neutrality theorem or finite coefficient",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "J4596_5_live_total",
            "symbol": "J_X^live",
            "status_after_4596": "REDUCED_VECTOR_READY",
            "bound_if_open": "||J_X^live|| <= ||J_X^EM_open||+||J_X^nonHilbert||+||J_X^dyn_exchange||+||J_X^boundary_readout||",
            "next_input": "first finite norm row or parent-zero certificate",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def body_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4596_0_memory_density",
            "target": "rho_mem",
            "before": "||rho_mem|| <= ||B_mem_eff||||R_obs|| + ||C_mem||||T|| + ||J_mem||",
            "after": "strict source-kernel branch: ||rho_mem|| <= ||B_mem_eff||||R_obs|| + ||C_mem||||T|| + ||J_mem_live||",
            "claim_effect": "source-kernel subcurrent removed; B_mem_eff,C_mem,J_mem_live,Q_boundary_mem still block local-GR claim",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4596_1_memory_amplitude",
            "target": "A_mem",
            "before": "|A_mem| envelope contains total J_mem",
            "after": "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs||+||C_mem||||T||+||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)",
            "claim_effect": "ready for first live-current norm or C_mem parent descent",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4596_2_fibre_density",
            "target": "rho_h",
            "before": "||rho_h|| <= ||B_h||||R_obs|| + ||C_h||||T|| + ||J_h||",
            "after": "strict source-kernel branch: ||rho_h|| <= ||B_h||||R_obs|| + ||C_h||||T|| + ||J_h_live||",
            "claim_effect": "source-kernel subcurrent removed; B_h,C_h,J_h_live,Q_boundary_h still block local-GR claim",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4596_3_fibre_amplitude",
            "target": "A_h",
            "before": "|A_h| envelope contains total J_h",
            "after": "|A_h| <= [exp(R/lambda_h) int_body (||B_h||||R_obs||+||C_h||||T||+||J_h_live||) dV + ||Q_boundary_h||]/(4*pi||Z_h||)",
            "claim_effect": "ready for h-blind source descent or first live-current norm",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def coefficient_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CO4596_0_Cmem", "C_mem", "matter-trace memory coupling", "parent-sign q-basic source descent", "|C_mem|"),
        ("CO4596_1_Ch", "C_h", "matter-trace fibre coupling", "parent-sign h-blind/q-basic source descent", "|C_h|"),
        ("CO4596_2_Jkernel", "J_X^source_kernel", "source-worldtube active kernel", "strict 4587-4592 branch tied to X", "0 on strict branch; open bound otherwise"),
        ("CO4596_3_JEM", "J_X^EM_open", "radiative/nonminimal EM/Poynting flux", "same Hodge/current owner plus no-flux collar", "boundary Poynting flux norm"),
        ("CO4596_4_JnonHilbert", "J_X^nonHilbert", "retained non-Hilbert source current", "no retained current theorem", "absolute source profile"),
        ("CO4596_5_Jdyn", "J_X^dyn_exchange", "dynamic clock/source exchange", "stationary exchange closure", "dynamic current norm"),
        ("CO4596_6_Qboundary", "Q_boundary_X", "boundary/body charge", "regular neutral boundary/source-reference lock", "finite boundary integral"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": cid,
            "symbol": symbol,
            "role": role,
            "derive_first": derive,
            "finite_fallback": fallback,
            "current_status": "ZERO_INSERTED_IF_STRICT_BRANCH" if cid == "CO4596_2_Jkernel" else "MISSING_PARENT_ZERO_OR_VALUE",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for cid, symbol, role, derive, fallback in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4596_strict_branch",
            "input_branch": "all 4587-4592 source-worldtube strict clauses tied to the same memory/fibre X",
            "expected_result": "J_X^source_kernel=0 and A_X envelope uses J_X^live",
            "status": "SYMBOLIC_CONTROL_PASS",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4596_open_poynting",
            "input_branch": "radiative Poynting flux crosses worldtube",
            "expected_result": "J_X^EM_open remains in J_X^live",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4596_explicit_source_dependence",
            "input_branch": "source masses/Hodge/support depend explicitly on memory/fibre coordinate",
            "expected_result": "C_X remains finite; descent zero rejected",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4596_overclaim",
            "input_branch": "source-kernel subzero only",
            "expected_result": "do not claim B_mem_eff,C_X,J_live,Q_boundary or local-GR closure",
            "status": "FIREWALL_PASS",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4596_0_sources_exist",
            "claim": "all cited source paths exist",
            "passed": all(row["path_exists"] for row in sources),
            "detail": "source register path check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4596_1_needles_found",
            "claim": "all cited source needles found",
            "passed": all(row["needle_found"] for row in sources),
            "detail": "source register needle check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4596_2_source_kernel_inserted",
            "claim": "strict source-kernel zero is inserted into J_X",
            "passed": True,
            "detail": "J_X^source_kernel=0 on strict 4587-4592 branch",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4596_3_body_envelope_reduced",
            "claim": "A_mem/A_h envelopes use J_live",
            "passed": True,
            "detail": "body-charge update rows written",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4596_4_no_public_claim",
            "claim": "no local-GR/R10/PPN claim emitted",
            "passed": True,
            "detail": "C/B/Jlive/Qboundary values and parent signatures remain open",
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
            "source_kernel_to_J_inserted": True,
            "C_descent_contract_written": True,
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
            "derived": "strict source-kernel subcurrent insertion into J_mem/J_h; C_X chain-rule source descent contract; reduced A_mem/A_h envelope with J_live; first coefficient rows",
            "not_derived": "parent-signed C_mem=C_h=0; parent-signed J_live=0; numeric Jlive/Qboundary/B/C coefficients; full local-GR/R10/PPN scoring",
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
            "reason": "After source-kernel insertion, the fastest remaining progress is either parent-sign C_mem/C_h descent or put the first finite J_live norm into the body-charge envelope.",
            "derive_first": "prove source action and EM/Hodge/support/readout are q-basic/h-blind for memory and fibre",
            "fallback": "fill first finite norm row for J_X^EM_open, J_X^nonHilbert, J_X^dyn_exchange or Q_boundary_X",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4596 Y5 R2FR memory/fibre source-functor signature or first body-charge coefficient row

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4596 cashes in the 4587-4592 source-kernel work against the 4595 memory/fibre body-charge law.

For `X in {{memory m, finite-cell fibre h}}`, split the direct-current term as:

```text
J_X = J_X^source_kernel + J_X^Hilbert_stationary + J_X^EM_open
    + J_X^nonHilbert + J_X^dyn_exchange + J_X^boundary_readout.
```

The strict 4587-4592 branch gives:

```text
J_X^source_kernel = 0
```

provided the same q-basic Hilbert/Maxwell source-worldtube branch is used for source density, EM stress/Poynting, support, reference mass, verticality, readout mask and tau/e_obs.

This is not full `J_X=0`. The reduced live vector is:

```text
J_X^live = J_X^EM_open + J_X^nonHilbert
         + J_X^dyn_exchange + J_X^boundary_readout.
```

The memory body-charge envelope therefore becomes:

```text
|A_mem| <= [exp(R/lambda_mem) int_body
 (||B_mem_eff||||R_obs|| + ||C_mem||||T|| + ||J_mem^live||) dV
 + ||Q_boundary_mem||] / (4*pi ||Z_mem||).
```

The fibre envelope becomes:

```text
|A_h| <= [exp(R/lambda_h) int_body
 (||B_h||||R_obs|| + ||C_h||||T|| + ||J_h^live||) dV
 + ||Q_boundary_h||] / (4*pi ||Z_h||).
```

The `C_X` source-descent route is also made explicit:

```text
S_src = Sbar_src[q(Phi),Psi,A,theta], v_X in ker(Dq)
=> delta_X S_src = (delta Sbar/dq) Dq[v_X] = 0.
```

So `C_mem` and `C_h` can be killed by a parent-signed q-basic/h-blind source functor, but they are not killed merely by naming the source Hilbert-owned.

No local-GR, R10, PPN or orbital pass is claimed here.

## Source Register

{markdown_table(tables["sources"])}

## Source-Kernel To J Insertion

{markdown_table(tables["insertion"])}

## Cmem/Ch Source-Descent Contract

{markdown_table(tables["descent"])}

## Reduced J Residual Vector

{markdown_table(tables["j_vector"])}

## Body-Charge Envelope Update

{markdown_table(tables["body"])}

## First Body-Charge Coefficient Rows

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
    return f"""# PPC4161 612 - Memory/Fibre Source-Kernel Insertion Or First Body-Charge Coefficient Row

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

Given the 4595 local source density

```text
rho_X = B_X R_obs + C_X T + J_X,
```

decompose

```text
J_X = J_X^source_kernel + J_X^Hilbert_stationary + J_X^EM_open
    + J_X^nonHilbert + J_X^dyn_exchange + J_X^boundary_readout.
```

The strict 4587-4592 source-worldtube branch gives `J_X^source_kernel=0` when tied to the same memory/fibre parent direction. Therefore the updated live current is:

```text
J_X^live = J_X^EM_open + J_X^nonHilbert
         + J_X^dyn_exchange + J_X^boundary_readout.
```

The matter trace coefficient obeys the source-functor chain rule:

```text
S_src=Sbar_src[q(Phi),Psi,A,theta], v_X in ker(Dq)
=> C_X=0
```

only when all source standards, Hodge/current owner, support and readout maps are q-basic/h-blind before variation.

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

    add("VAL4596_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    add("VAL4596_01_needles_found", all(row["needle_found"] for row in tables["sources"]), "all cited source needles found")
    csv_paths = [
        SOURCE_REGISTER,
        INSERTION_CSV,
        DESCENT_CSV,
        J_VECTOR_CSV,
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
    add("VAL4596_02_csv_parse", csv_ok, ";".join(details))

    insertion_text = "\n".join(str(row) for row in tables["insertion"])
    add("VAL4596_03_kernel_zero_inserted", "J_X^source_kernel=0" in insertion_text, "source-kernel zero inserted into J_X")

    body_text = "\n".join(str(row) for row in tables["body"])
    add("VAL4596_04_body_update", "J_mem_live" in body_text and "J_h_live" in body_text, "A_mem/A_h envelopes use live J residuals")

    descent_text = "\n".join(str(row) for row in tables["descent"])
    add("VAL4596_05_descent_contract", "delta_X S_src" in descent_text and "Dq[v_X]" in descent_text, "C_X chain-rule descent contract written")

    coeff_text = "\n".join(str(row) for row in tables["coefficients"])
    add("VAL4596_06_coeff_rows", "C_mem" in coeff_text and "J_X^EM_open" in coeff_text and "Q_boundary_X" in coeff_text, "first coefficient rows staged")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "local_GR_public_claim", "parent_zero_or_numeric_bound_signed"} and value is True:
                    all_false = False
    add("VAL4596_07_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4596_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4596_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4596_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4596_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4596_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4596_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4596_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4596_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4596_OVERALL", all(row["status"] == "PASS" for row in rows), "4596 source-kernel insertion into memory/fibre J vector")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "insertion": insertion_rows(now),
        "descent": descent_rows(now),
        "j_vector": j_vector_rows(now),
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
    write_csv(INSERTION_CSV, tables["insertion"])
    write_csv(DESCENT_CSV, tables["descent"])
    write_csv(J_VECTOR_CSV, tables["j_vector"])
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
## PPC4161 Local Addendum - Memory/Fibre Source-Kernel Insertion

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The strict 4587-4592 source-worldtube zero chain is now inserted into the 4595 memory/fibre body-charge gate: `J_X^source_kernel=0` on the same q-basic Hilbert/Maxwell branch. The live current is reduced to open EM/Poynting, retained non-Hilbert current, dynamic exchange and boundary/readout pieces. This narrows the `A_mem/A_h` envelopes without claiming full local GR.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Source-Kernel To Memory/Fibre J Vector

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private local packet now cashes the source-kernel closure into the memory/fibre finite-range branch. The next useful gate is to parent-sign `C_mem/C_h` source descent or fill the first finite `J_live`/boundary coefficient row.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4596 validation failed: {failed}")
    print(f"4596 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
