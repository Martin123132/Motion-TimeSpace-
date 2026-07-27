from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4684"
CLAIM_ID = "L-526"
MARKER = "PPC4161_MEMORY_FIBRE_SOURCE_KERNEL_INSERTION_CURRENT_BRANCH_4684"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_FIBRE_SOURCE_KERNEL_INSERTION_CURRENT_BRANCH_4684"
DECISION = "STRICT_SOURCE_KERNEL_INSERTED_INTO_MEMORY_FIBRE_J_VECTOR_LIVE_CX_JLIVE_ENVELOPE_REDUCED_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md"

DOC_PATH = POST / "4684-Y5-R2FR-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md"
FORMAL_PATH = FORMAL / "700-PPC4161-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4683_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4683_NEXT_TARGET.csv"
CSV_4683_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4683_STATUS.csv"
CSV_4596_INSERTION = SOURCE_DIR / "P8_Y5_R2FR_4596_SOURCE_KERNEL_TO_JMEM_INSERTION.csv"
CSV_4596_DESCENT = SOURCE_DIR / "P8_Y5_R2FR_4596_CMEM_CH_SOURCE_DESCENT_CONTRACT.csv"
CSV_4596_JVECTOR = SOURCE_DIR / "P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv"
CSV_4596_BODY = SOURCE_DIR / "P8_Y5_R2FR_4596_BODY_CHARGE_ENVELOPE_UPDATE.csv"
CSV_4596_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv"
CSV_4596_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4596_STATUS.csv"
CSV_4596_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4596_NEXT_TARGET.csv"
CSV_4596_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4596_VALIDATION.csv"
CSV_4597_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4597_STATUS.csv"
CSV_4597_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4597_NEXT_TARGET.csv"
CSV_4597_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4597_VALIDATION.csv"
FORMAL_612 = FORMAL / "612-PPC4161-memory-fibre-source-kernel-insertion-or-first-body-charge-coefficient-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4684_SOURCE_REGISTER.csv"
INSERTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_SOURCE_KERNEL_TO_JMEM_INSERTION.csv"
DESCENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_CMEM_CH_SOURCE_DESCENT_CONTRACT.csv"
JVECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv"
BODY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_BODY_CHARGE_ENVELOPE_UPDATE.csv"
COEFF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4684_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4684_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4684_00_4683_next", CSV_4683_NEXT, "4684-Y5-R2FR-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md", "4683 selected source-functor target."),
        ("SRC4684_01_4683_status", CSV_4683_STATUS, "MEMORY_FIBRE_ZERO_SWITCH", "4683 status."),
        ("SRC4684_02_4596_insertion", CSV_4596_INSERTION, "INS4596_0_common_split", "source-kernel insertion law."),
        ("SRC4684_03_4596_descent", CSV_4596_DESCENT, "DS4596_0_chain_rule", "C_X chain-rule descent contract."),
        ("SRC4684_04_4596_jvector", CSV_4596_JVECTOR, "J4596_5_live_total", "J_live reduced vector."),
        ("SRC4684_05_4596_body", CSV_4596_BODY, "BU4596_1_memory_amplitude", "A_mem/A_h envelope update."),
        ("SRC4684_06_4596_coeff", CSV_4596_COEFF, "CO4596_6_Qboundary", "first coefficient rows staged."),
        ("SRC4684_07_4596_status", CSV_4596_STATUS, "STRICT_SOURCE_KERNEL_INSERTED", "4596 status."),
        ("SRC4684_08_4596_next", CSV_4596_NEXT, "4597-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md", "4596 next target."),
        ("SRC4684_09_4596_validation", CSV_4596_VALIDATION, "VAL4596_OVERALL", "4596 validation passed."),
        ("SRC4684_10_4597_status", CSV_4597_STATUS, "CMEM_CH_QBASIC_SOURCE_DESCENT", "4597 q-basic descent already exists."),
        ("SRC4684_11_4597_next", CSV_4597_NEXT, "constant-standard-source-weight-zero-or-CXlive-first-norm", "4597 next target."),
        ("SRC4684_12_4597_validation", CSV_4597_VALIDATION, "VAL4597_OVERALL", "4597 validation passed."),
        ("SRC4684_13_formal612", FORMAL_612, "J_X^live = J_X^EM_open", "formal source-kernel insertion."),
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
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def insertion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "insertion_id": "INS4684_0_common_split",
            "target": "memory/fibre direct current",
            "formula": "J_X = J_X^source_kernel + J_X^Hilbert_stationary + J_X^EM_open + J_X^nonHilbert + J_X^dyn_exchange + J_X^boundary_readout",
            "zero_condition": "same q-basic Hilbert/Maxwell worldtube branch; public Maxwell-Hodge EM in T_total; compact regular support; source-blind Href; certified Dq verticality; fixed readout mask; same tau/e_obs",
            "consequence": "J_X^source_kernel=0 and Hilbert stationary current contributes no extra direct memory/fibre current",
            "status": "SOURCE_KERNEL_SUBCURRENT_ZERO_INSERTED_CONDITIONALLY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "insertion_id": "INS4684_1_memory",
            "target": "J_mem",
            "formula": "J_mem_live = J_mem^EM_open + J_mem^nonHilbert + J_mem^dyn_exchange + J_mem^boundary_readout",
            "zero_condition": "strict source-kernel clauses fire and all live current subchannels are independently zero",
            "consequence": "A_mem envelope drops source-kernel subterm but retains J_mem_live",
            "status": "MEMORY_J_VECTOR_REDUCED_NOT_CLOSED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "insertion_id": "INS4684_2_fibre",
            "target": "J_h",
            "formula": "J_h_live = J_h^EM_open + J_h^nonHilbert + J_h^dyn_exchange + J_h^boundary_readout",
            "zero_condition": "same source-kernel branch plus h-blind source functor and no retained fibre current",
            "consequence": "A_h envelope drops source-kernel subterm but retains J_h_live",
            "status": "FIBRE_J_VECTOR_REDUCED_NOT_CLOSED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def descent_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DS4684_0_chain_rule", "C_X", "If S_src=Sbar_src[q(Phi),Psi,A,theta] and v_X in ker(Dq), then delta_X S_src=(delta Sbar/dq)Dq[v_X]=0.", "source action, masses, clocks, EM Hodge/current owner and support/readout are all q-basic before variation", "|C_X T| retained as an absolute body-charge density term", "EXACT_CHAIN_RULE_CONTRACT_NOT_PARENT_SIGNED_FOR_ALL_X"),
        ("DS4684_1_memory", "C_mem", "memory/class scalar is matter-trace silent if it is a vertical memory coordinate of q and active source functor descends through q", "v_m in ker(Dq); no explicit m-dependence in masses/standards/Hodge/support/readout", "|C_mem| ||T|| remains in A_mem", "CONDITIONAL_ZERO_ROUTE_READY_PARENT_SIGNATURE_UNSIGNED"),
        ("DS4684_2_fibre", "C_h", "finite-cell fibre is matter-trace silent if h is absent from source grammar or eliminated before source functor is varied", "h-blind S_src or h vertical to q plus no source standards/hodge/support dependence", "|C_h| ||T|| remains in A_h", "CONDITIONAL_ZERO_ROUTE_READY_PARENT_SIGNATURE_UNSIGNED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "coefficient": coefficient,
            "derivation": derivation,
            "zero_condition": zero_condition,
            "fallback": fallback,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, coefficient, derivation, zero_condition, fallback, status in data
    ]


def jvector_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("J4684_0_source_kernel", "J_X^source_kernel", "ZERO_ON_STRICT_BRANCH", "L_JX L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux)", "same-branch certificate tying source-worldtube clauses to memory/fibre X"),
        ("J4684_1_EM_open", "J_X^EM_open", "ZERO_ONLY_FOR_MAXWELL_HODGE_NO_FLUX_BRANCH", "|int_boundary T_EM(tau,n)dSigma dt|/|M_H_ref| times source-coupling operator norm", "no-radiation collar or finite Poynting flux profile"),
        ("J4684_2_nonHilbert", "J_X^nonHilbert", "LIVE", "||J_X^nonHilbert|| absolute source profile", "prove no retained non-Hilbert source current or fill finite profile"),
        ("J4684_3_dynamic_exchange", "J_X^dyn_exchange", "LIVE_OUTSIDE_STATIONARY_BRANCH", "||exchange/clock/source current||", "stationary exchange closure or finite dynamic current row"),
        ("J4684_4_boundary_readout", "J_X^boundary_readout", "LIVE_UNLESS_BOUNDARY_READOUT_NEUTRAL", "||boundary/readout source reference shift||", "boundary/reference neutrality theorem or finite coefficient"),
        ("J4684_5_live_total", "J_X^live", "REDUCED_VECTOR_READY", "||J_X^live|| <= ||J_X^EM_open||+||J_X^nonHilbert||+||J_X^dyn_exchange||+||J_X^boundary_readout||", "first finite norm row or parent-zero certificate"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": residual_id,
            "symbol": symbol,
            "status_after_4684": status,
            "bound_if_open": bound,
            "next_input": next_input,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for residual_id, symbol, status, bound, next_input in data
    ]


def body_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BU4684_0_memory_density", "rho_mem", "||rho_mem|| <= ||B_mem_eff||||R_obs|| + ||C_mem||||T|| + ||J_mem||", "strict source-kernel branch: ||rho_mem|| <= ||B_mem_eff||||R_obs|| + ||C_mem||||T|| + ||J_mem_live||", "source-kernel subcurrent removed; B_mem_eff,C_mem,J_mem_live,Q_boundary_mem still block local-GR claim"),
        ("BU4684_1_memory_amplitude", "A_mem", "|A_mem| envelope contains total J_mem", "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs||+||C_mem||||T||+||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)", "ready for first live-current norm or C_mem parent descent"),
        ("BU4684_2_fibre_density", "rho_h", "||rho_h|| <= ||B_h||||R_obs|| + ||C_h||||T|| + ||J_h||", "strict source-kernel branch: ||rho_h|| <= ||B_h||||R_obs|| + ||C_h||||T|| + ||J_h_live||", "source-kernel subcurrent removed; B_h,C_h,J_h_live,Q_boundary_h still block local-GR claim"),
        ("BU4684_3_fibre_amplitude", "A_h", "|A_h| envelope contains total J_h", "|A_h| <= [exp(R/lambda_h) int_body (||B_h||||R_obs||+||C_h||||T||+||J_h_live||) dV + ||Q_boundary_h||]/(4*pi||Z_h||)", "ready for h-blind source descent or first live-current norm"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "target": target,
            "before": before,
            "after": after,
            "claim_effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, target, before, after, effect in data
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CO4684_0_Cmem", "C_mem", "matter-trace memory coupling", "parent-sign q-basic source descent", "|C_mem|", "MISSING_PARENT_ZERO_OR_VALUE"),
        ("CO4684_1_Ch", "C_h", "matter-trace fibre coupling", "parent-sign h-blind/q-basic source descent", "|C_h|", "MISSING_PARENT_ZERO_OR_VALUE"),
        ("CO4684_2_Jkernel", "J_X^source_kernel", "source-worldtube active kernel", "strict source-kernel branch tied to X", "0 on strict branch; open bound otherwise", "ZERO_INSERTED_IF_STRICT_BRANCH"),
        ("CO4684_3_JEM", "J_X^EM_open", "radiative/nonminimal EM/Poynting flux", "same Hodge/current owner plus no-flux collar", "boundary Poynting flux norm", "MISSING_PARENT_ZERO_OR_VALUE"),
        ("CO4684_4_JnonHilbert", "J_X^nonHilbert", "retained non-Hilbert source current", "no retained current theorem", "absolute source profile", "MISSING_PARENT_ZERO_OR_VALUE"),
        ("CO4684_5_Jdyn", "J_X^dyn_exchange", "dynamic clock/source exchange", "stationary exchange closure", "dynamic current norm", "MISSING_PARENT_ZERO_OR_VALUE"),
        ("CO4684_6_Qboundary", "Q_boundary_X", "boundary/body charge", "regular neutral boundary/source-reference lock", "finite boundary integral", "MISSING_PARENT_ZERO_OR_VALUE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "role": role,
            "derive_first": derive_first,
            "finite_fallback": finite_fallback,
            "current_status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for coefficient_id, symbol, role, derive_first, finite_fallback, status in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4684_0_Cmem_Ch", "C_mem/C_h source-functor descent", "chain-rule route written; q-basic/h-blind parent signatures missing", NEXT_TARGET),
        ("SURV4684_1_Jlive", "J_X live direct current", "source-kernel removed on strict branch; EM_open/nonHilbert/dyn/boundary live", NEXT_TARGET),
        ("SURV4684_2_memory_fibre_body_charge", "A_mem/A_h body-charge envelope", "reduced envelope with J_live; B/C/J/Q inputs remain finite", NEXT_TARGET),
        ("SURV4684_3_cR2_MR", "c_R2/M_R finite-range branch", "pressure now routed through memory/fibre source coefficients", "continue source-functor descent before returning to R10 scoring"),
        ("SURV4684_4_global_parent", "EH/global parent/material projection", "unchanged public blockers", "keep promotion firewall active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4684": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4684_0", "Do not set all J_X to zero when only the strict source-kernel subcurrent is zero."),
        ("CTRL4684_1", "C_mem/C_h vanish only if the whole source functor is q-basic/h-blind before variation."),
        ("CTRL4684_2", "EM/Poynting can remain in J_X^EM_open unless same-Hodge/current/no-flux guards fire."),
        ("CTRL4684_3", "Body-charge envelopes must use absolute live terms; no cancellation between B, C, J and boundary pieces."),
        ("CTRL4684_4", "Next target is C_mem/C_h q-basic split or first J_live norm, not a broad cR2 rerun."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "rule": rule,
            "status": "ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, rule in controls
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4684 imports the 4596 source-kernel insertion into the current branch. The strict source-kernel subcurrent is zero only on the same q-basic/Hodge/worldtube/readout branch. The live memory/fibre currents are J_X^EM_open, J_X^nonHilbert, J_X^dyn_exchange and J_X^boundary_readout. C_mem/C_h have a clean chain-rule zero route, but only if the source functor is q-basic/h-blind before variation. The next target is the Cmem/Ch q-basic split or first finite J_live norm.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "strict source-kernel subcurrent insertion into J_mem/J_h; C_X chain-rule source descent contract; reduced A_mem/A_h envelope with J_live; first coefficient rows",
            "not_derived": "parent-signed C_mem=C_h=0; parent-signed J_live=0; numeric Jlive/Qboundary/B/C coefficients; full local-GR/R10/PPN scoring",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4684_0",
            "target": NEXT_TARGET,
            "reason": "After source-kernel insertion, the fastest remaining progress is either parent-sign C_mem/C_h descent or put the first finite J_live norm into the body-charge envelope.",
            "derive_first": "prove source action and EM/Hodge/support/readout are q-basic/h-blind for memory and fibre",
            "fallback": "fill first finite norm row for J_X^EM_open, J_X^nonHilbert, J_X^dyn_exchange or Q_boundary_X",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4684 - Y5/R2FR Memory/Fibre Source-Functor Signature Or First Body-Charge Coefficient Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4684 imports the source-kernel insertion into the current memory/fibre branch.

```text
J_X = J_X^source_kernel + J_X^Hilbert_stationary + J_X^EM_open
    + J_X^nonHilbert + J_X^dyn_exchange + J_X^boundary_readout

strict branch => J_X^source_kernel = 0

J_X^live = J_X^EM_open + J_X^nonHilbert
         + J_X^dyn_exchange + J_X^boundary_readout.
```

The matter-trace coefficient has the clean chain-rule route:

```text
S_src = Sbar_src[q(Phi), Psi, A, theta],  v_X in ker(Dq)
=> C_X = 0
```

but only when source standards, EM Hodge/current owner, support and readout maps are q-basic/h-blind before variation.

## Source Register

{table(rows["sources"])}

## Source-Kernel Insertion

{table(rows["insertions"])}

## Cmem / Ch Source-Descent Contract

{table(rows["descent"])}

## Jmem / Jh Reduced Residual Vector

{table(rows["jvector"])}

## Body-Charge Envelope Update

{table(rows["body"])}

## First Body-Charge Coefficient Rows

{table(rows["coefficients"])}

## Survivor Update

{table(rows["survivors"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4684 - Y5/R2FR", "# 700 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4684 imports the source-kernel insertion into the current memory/fibre branch. The strict source-kernel subcurrent is zero only on the same q-basic/Hodge/worldtube/readout branch; J_X^live remains EM_open + nonHilbert + dynamic_exchange + boundary_readout. C_mem/C_h have a chain-rule zero route only if the full source functor is q-basic/h-blind before variation.",
                "current_evidence": "Generated source register, source-kernel insertion, Cmem/Ch source-descent contract, Jmem/Jh reduced residual vector, body-charge envelope update, coefficient rows, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Treating strict source-kernel zero as total J_X zero, or setting C_mem/C_h to zero without source standards/Hodge/support/readout q-basic descent.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current Memory/Fibre Source-Kernel Insertion

Marker: `{MARKER}`

4684 inserts the strict source-kernel zero into the memory/fibre current vector:

```text
J_X^live = J_X^EM_open + J_X^nonHilbert
         + J_X^dyn_exchange + J_X^boundary_readout.
```

The `C_mem/C_h` chain-rule zero route is also explicit, but requires the source functor and standards/Hodge/support/readout maps to be q-basic/h-blind before variation. The next target is the q-basic split or first finite `J_live` norm.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Memory/Fibre Source-Kernel Insertion

Marker: `{PACKET_MARKER}`

The packet now carries the reduced live memory/fibre current `J_X^live` and the exact `C_X` chain-rule descent contract. Do not collapse live EM/open, non-Hilbert, dynamic or boundary currents without a parent certificate or finite norm.

- insertion csv: `{INSERTION_CSV.name}`
- j-vector csv: `{JVECTOR_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4684_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4684_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4684_2_source_kernel_inserted", any(row["insertion_id"] == "INS4684_0_common_split" for row in rows["insertions"]), "source-kernel split inserted"),
        ("VAL4684_3_chain_rule_contract", any(row["contract_id"] == "DS4684_0_chain_rule" for row in rows["descent"]), "C_X chain-rule contract written"),
        ("VAL4684_4_jlive_vector", any(row["symbol"] == "J_X^live" for row in rows["jvector"]), "J_live reduced vector present"),
        ("VAL4684_5_body_update", len(rows["body"]) == 4, "A_mem/A_h envelope update present"),
        ("VAL4684_6_coeff_rows", len(rows["coefficients"]) == 7, "first coefficient rows staged"),
        ("VAL4684_7_next_cmem_ch", rows["next"][0]["target"] == NEXT_TARGET, "next Cmem/Ch target selected"),
        ("VAL4684_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-526"),
        ("VAL4684_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4684_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4684_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4684_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4684_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4684_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4684_13_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4684_14_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4684_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "insertions": insertion_rows(timestamp),
        "descent": descent_rows(timestamp),
        "jvector": jvector_rows(timestamp),
        "body": body_rows(timestamp),
        "coefficients": coefficient_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        INSERTION_CSV: rows["insertions"],
        DESCENT_CSV: rows["descent"],
        JVECTOR_CSV: rows["jvector"],
        BODY_CSV: rows["body"],
        COEFF_CSV: rows["coefficients"],
        SURVIVOR_CSV: rows["survivors"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
