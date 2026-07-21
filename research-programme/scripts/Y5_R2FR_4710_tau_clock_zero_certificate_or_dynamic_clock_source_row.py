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

CHECKPOINT = "4710"
CLAIM_ID = "L-552"
MARKER = "PPC4161_TAU_CLOCK_ZERO_CERTIFICATE_OR_DYNAMIC_CLOCK_SOURCE_ROW_4710"
PACKET_MARKER = "PPC4161_PACKET_TAU_CLOCK_ZERO_CERTIFICATE_OR_DYNAMIC_CLOCK_SOURCE_ROW_4710"
DECISION = "EXACT_ROOT_BYPASS_DERIVED_TAU_ZERO_NOT_NEEDED_IF_RQ_ZERO_SOURCE_ROWS_RETAINED_NONCLAIM"
NEXT_TARGET = "4711-Y5-R2FR-exact-root-local-residual-certificate-or-finite-clock-inputs.md"

DOC_PATH = POST / "4710-Y5-R2FR-tau-clock-zero-certificate-or-dynamic-clock-source-row.md"
FORMAL_PATH = FORMAL / "726-PPC4161-tau-clock-zero-certificate-or-dynamic-clock-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4709_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4709_NEXT_TARGET.csv"
CSV_4709_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4709_CLOCK_TAU_MAP_THEOREM_ROWS.csv"
CSV_4709_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4709_CLOCK_PRODUCT_ISOLATION_ROWS.csv"
CSV_4709_BREADOUT = SOURCE_DIR / "P8_Y5_R2FR_4709_DYNAMIC_BREADOUT_SOURCE_ROW_TEMPLATE.csv"
CSV_4709_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4709_TRANSFER_FIREWALL_ROWS.csv"
CSV_4709_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4709_VALIDATION.csv"
CSV_647_TAU = SOURCE_DIR / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv"
CSV_647_CHIX = SOURCE_DIR / "P8_Y5_R10_647_CHIX_DEFINITION_ATTEMPT.csv"
CSV_648_DYN = SOURCE_DIR / "P8_Y5_R10_648_LOCAL_CHIX_DYNAMICS_ATTEMPT.csv"
CSV_648_REQ = SOURCE_DIR / "P8_Y5_R10_648_TAU_SURVIVAL_REQUIREMENTS.csv"
CSV_648_GATES = SOURCE_DIR / "P8_Y5_R10_648_LOCAL_SILENCE_DECISION_GATES.csv"
CSV_3228_XI = SOURCE_DIR / "P8_Y5_R2FR_3228_XI_CLOCK_PRODUCT_DERIVATION.csv"
CSV_3228_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_3228_PARENT_XI_CLOCK_CONTRACT.csv"
CSV_3228_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3228_XI_CLOCK_BOUND_INTERFACE.csv"
CSV_3229_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_3229_XI_CLOCK_REDUCTION_WITH_TRANSPORT_ERROR.csv"
CSV_3229_TRANSPORT = SOURCE_DIR / "P8_Y5_R2FR_3229_TRANSPORT_IDENTITY_DERIVATION.csv"
CSV_4660_DYN = SOURCE_DIR / "P8_Y5_R2FR_4660_DYNAMIC_CLOCK_REDSHIFT_BOUND_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4710_SOURCE_REGISTER.csv"
ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4710_TAU_ZERO_OR_EXACT_ROOT_BYPASS_CERTIFICATE.csv"
FINITE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4710_DYNAMIC_CLOCK_FINITE_SOURCE_ROWS.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4710_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4710_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4710_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4710_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4710_VALIDATION.csv"


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
        ("SRC4710_00_4709_next", CSV_4709_NEXT, "NT4709_0", "4709 handoff to tau zero or dynamic source row"),
        ("SRC4710_01_4709_tau_zero", CSV_4709_THEOREM, "CTM4709_0_observed_coframe_tau_zero", "observed proper-time zero theorem"),
        ("SRC4710_02_4709_clock_zero", CSV_4709_THEOREM, "CTM4709_3_clock_Breadout_zero_branch", "clock-sector B_readout zero"),
        ("SRC4710_03_4709_product", CSV_4709_PRODUCT, "CPI4709_0_product_bound_law", "clock product-only bound law"),
        ("SRC4710_04_4709_dynamic_source", CSV_4709_BREADOUT, "BRS4709_2_dynamic_clock_source_contract", "dynamic clock source row template"),
        ("SRC4710_05_4709_firewall", CSV_4709_FIREWALL, "FW4709_0_no_clock_product_to_Breadout", "product-to-standalone firewall"),
        ("SRC4710_06_4709_validation", CSV_4709_VALIDATION, "VAL4709_OVERALL", "4709 validation"),
        ("SRC4710_07_647_tau_map", CSV_647_TAU, "TAU647_0_time_drift", "tau_clock_time definition"),
        ("SRC4710_08_647_local_silence", CSV_647_TAU, "TAU647_3_local_silence", "local silence tau zero candidate"),
        ("SRC4710_09_647_chix_root", CSV_647_CHIX, "CHX647_3_strict_local_silence", "chi_X constant local candidate"),
        ("SRC4710_10_648_strict", CSV_648_DYN, "LCD648_0_strict_local_coframe", "strict coframe local silence attempt"),
        ("SRC4710_11_648_closed", CSV_648_DYN, "LCD648_1_closed_gapped_boundary_state", "closed/gapped local silence attempt"),
        ("SRC4710_12_648_gate", CSV_648_GATES, "LSD648_1_local_silence_theorem", "local silence theorem still missing"),
        ("SRC4710_13_648_ultra", CSV_648_GATES, "LSD648_3_ultra_screening_requirement", "dynamic ultra-screening requirement"),
        ("SRC4710_14_3228_product", CSV_3228_XI, "XID3228_3_root_taylor_product", "near-root clock product law"),
        ("SRC4710_15_3228_xi", CSV_3228_XI, "XID3228_4_xi_clock_identity", "Xi_clock identity"),
        ("SRC4710_16_3228_exact_root", CSV_3228_XI, "XID3228_5_exact_root_silence", "exact-root alpha silence route"),
        ("SRC4710_17_3228_transport_owner", CSV_3228_CONTRACT, "XIC3228_3_same_branch_transport", "same-branch transport owner missing"),
        ("SRC4710_18_3228_data_ready", CSV_3228_CONTRACT, "XIC3228_5_data_comparison", "clock-bound data side ready"),
        ("SRC4710_19_3228_bound", CSV_3228_BOUND, "XIB3228", "clock bound interface"),
        ("SRC4710_20_3229_reduction", CSV_3229_REDUCTION, "XIR3229_0_corrected_clock_reduction", "corrected finite clock reduction"),
        ("SRC4710_21_3229_transport_zero", CSV_3229_REDUCTION, "XIR3229_1_exact_transport_case", "exact transport zero"),
        ("SRC4710_22_3229_transport_finite", CSV_3229_REDUCTION, "XIR3229_2_finite_transport_case", "finite transport formula"),
        ("SRC4710_23_4660_dynamic_bound", CSV_4660_DYN, "BCB4660_1_clock_product_1sigma", "current best clock pressure gate"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "source_line": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "TZC4710_0_direct_tau_zero_sufficient_condition",
            "route": "direct tau_clock_time zero",
            "statement": "If chi_X=chi_bar(q_obs(Phi),theta_fixed) or chi_X is constant on a closed/gapped strict-local branch, and Dq_obs[T_clock]=0 along the local clock evolution, then tau_clock_time=d chi_X/d tau_obs=0.",
            "derivation": "The observed clock generator differentiates chi_X only through q_obs or fixed data. Chain rule gives D_T chi_X=(D chi_bar)Dq_obs[T_clock]=0.",
            "result": "tau_clock_time=0",
            "status": "EXACT_SUFFICIENT_CONDITION_PARENT_BRANCH_UNSIGNED",
            "why_not_enough": "The corpus has not yet parent-signed chi_X as q-basic or the closed/gapped strict-local branch as the final local domain.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "TZC4710_1_exact_root_bypass",
            "route": "exact residual-root bypass of tau zero",
            "statement": "If the local branch is an exact EM residual root R_Q=0, the EM kinetic owner is quadratic/no-linear in the residual norm, the 4709 clock readout branch is fixed, and the transport term has the 3229 ||R_Q|| prefactor, then D_tau ln alpha_EM=0 without assuming tau_clock_time=0.",
            "derivation": "3228 gives |D_tau ln alpha_EM| <= C_D |Delta m tau_clock_time| + E_HO + E_clock_transport. At an exact root Delta m=0 and R_Q=0; the product term vanishes, the higher-order term vanishes at the root, and E_clock_transport=(2|lambda_D|/Z_min)||R_Q||E_transport=0. 4709 also zeros the clock readout tail.",
            "result": "D_tau ln alpha_EM=0 while tau_clock_time may remain an unclaimed internal branch velocity",
            "status": "NEW_EXACT_CONDITIONAL_DERIVATION_BEST_ROUTE",
            "why_not_enough": "R_Q=0/no-linear kinetic owner/local exact-root branch still need parent certification before local-GR/clock pass can be claimed.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "TZC4710_2_product_zero_alternatives",
            "route": "Xi_clock factor zero",
            "statement": "Xi_clock=C_D |Delta m tau_clock_time| vanishes if C_D=0, Delta m=0, or tau_clock_time=0, but the theory must derive which factor is zero rather than fitting a cancellation.",
            "derivation": "This is the factor structure imported from 3228 and 4709. The cleanest current route is Delta m=0 via exact local residual root, not an assumed tau silence.",
            "result": "product-zero route map",
            "status": "DERIVED_FACTOR_STRUCTURE_NO_CANCELLATION",
            "why_not_enough": "Factor values are not source-backed; order-one tau or C_D with nonzero Delta m remains clock-pressured.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "TZC4710_3_transport_root_zero",
            "route": "transport tail root zero",
            "statement": "If E_clock_transport=(2|lambda_D|/Z_min)||R_Q||E_transport and the local branch has R_Q=0, then E_clock_transport=0 even if the raw transport error is not separately proved zero.",
            "derivation": "The corrected 3229 reduction carries a residual-amplitude prefactor. Exact residual root kills the clock transport contribution directly.",
            "result": "E_clock_transport=0 at exact root",
            "status": "EXACT_CONDITIONAL_TRANSPORT_BYPASS",
            "why_not_enough": "Requires the corrected 3229 prefactor and exact R_Q=0 to be parent-owned.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DCF4710_0_full_clock_residual_bound",
            "component": "clock_alpha_residual",
            "formula": "|D_tau ln alpha_EM| <= C_D |Delta m tau_clock_time| + E_HO + E_clock_transport + B_readout_clock",
            "value_or_bound": "",
            "units": "yr^-1",
            "source_path": f"{CSV_3228_XI};{CSV_3229_REDUCTION};{CSV_4709_THEOREM}",
            "missing_inputs": "C_D;Delta_m;tau_clock_time;E_HO;E_clock_transport unless exact-root branch signs",
            "status": "FINITE_DYNAMIC_SOURCE_ROW_TEMPLATE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DCF4710_1_exact_root_candidate",
            "component": "exact_root_clock_alpha_residual",
            "formula": "R_Q=0 and Delta m=0 and no-linear kinetic owner => |D_tau ln alpha_EM|=0",
            "value_or_bound": "0",
            "units": "yr^-1",
            "source_path": f"{CSV_3228_XI};{CSV_3229_REDUCTION};{CSV_4709_THEOREM}",
            "missing_inputs": "parent certificate for R_Q=0/no-linear kinetic owner/fixed observed clock branch",
            "status": "EXACT_CONDITIONAL_ZERO_CANDIDATE_NOT_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DCF4710_2_clock_pressure_gate",
            "component": "empirical_clock_pressure",
            "formula": "Xi_clock + E_HO + E_transport <= 2.1e-18",
            "value_or_bound": "2.1e-18",
            "units": "yr^-1",
            "source_path": f"{CSV_4660_DYN};{CSV_4709_PRODUCT};{CSV_3228_CONTRACT}",
            "missing_inputs": "split between Xi_clock, E_HO and E_transport, plus parent-side coefficient rows",
            "status": "DATA_SIDE_READY_PARENT_SIDE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DCF4710_3_ultra_screening_requirement",
            "component": "finite_tau_survival",
            "formula": "for |kappa_alpha|~1, |dchi_X/dN| must be <= 2.93e-8 relative to nominal H0 using the Yb row",
            "value_or_bound": "2.93e-8",
            "units": "dimensionless_H0_normalized_diagnostic",
            "source_path": f"{CSV_648_REQ};{CSV_648_GATES}",
            "missing_inputs": "physical kappa_alpha normalization and H0-to-lab tau map",
            "status": "DIAGNOSTIC_PRESSURE_NOT_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4710_0_no_assumed_tau_silence",
            "rule": "Do not set tau_clock_time=0 unless chi_X is q-basic/stationary or the closed/gapped strict-local branch is parent-signed.",
            "evidence": "TZC4710_0_direct_tau_zero_sufficient_condition;LSD648_1_local_silence_theorem",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4710_1_no_exact_root_claim_without_RQ",
            "rule": "The exact-root bypass is not a local-GR/clock pass unless R_Q=0, no-linear kinetic owner, and fixed observed-clock branch are all parent-certified.",
            "evidence": "TZC4710_1_exact_root_bypass;XID3228_5_exact_root_silence",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4710_2_no_product_split",
            "rule": "Do not split Xi_clock=C_D|Delta m tau_clock_time| into standalone factors without parent-owned C_D, Delta m and tau_clock_time rows.",
            "evidence": "TZC4710_2_product_zero_alternatives;CPI4709_1_Xi_identity",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_status_next(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_TAU_CLOCK_EXACT_ROOT_BYPASS_4710",
            "decision": DECISION,
            "reason": "Direct tau_clock_time=0 remains unsigned, but a stronger exact-root route is now derived: clock alpha drift vanishes at R_Q=0 with quadratic/no-linear EM kinetic owner and 4709 fixed clock readout, without assuming tau silence.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]
    status = [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "direct tau-zero sufficient condition; exact-root bypass D_tau ln alpha_EM=0; transport-root zero; finite dynamic clock source-row formula",
            "not_derived": "parent certificate for R_Q=0/no-linear kinetic owner; standalone tau_clock_time; finite C_D/Delta_m/E_HO/E_transport values; cross-arena transfer maps",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    next_rows = [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4710_0",
            "target": NEXT_TARGET,
            "reason": "The best route is no longer to force tau_clock_time=0; it is to prove the local residual exact-root certificate R_Q=0/no-linear EM kinetic owner, or fill finite C_D/Delta_m/tau/E_transport clock rows.",
            "derive_first": "prove exact local residual root R_Q=0 with no linear EM kinetic owner on the fixed observed-clock branch",
            "fallback": "source C_D, Delta_m, tau_clock_time, E_HO and E_clock_transport rows against the 2.1e-18 yr^-1 clock gate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4710 - Tau Clock Zero Certificate Or Dynamic Clock Source Row

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
4710 tries the direct `tau_clock_time -> 0` route first, but does not force it.

Direct tau-zero is a sufficient condition:

```text
chi_X = chi_bar(q_obs(Phi), theta_fixed)
Dq_obs[T_clock] = 0
=> tau_clock_time = d chi_X / d tau_obs = 0.
```

That branch is still unsigned because the corpus has not parent-certified `chi_X` as q-basic/stationary or the strict local closed/gapped domain.

The better route is the exact-root bypass:

```text
|D_tau ln alpha_EM| <= C_D |Delta m tau_clock_time| + E_HO + E_clock_transport + B_readout_clock
R_Q = 0, Delta m = 0, no linear EM kinetic owner
E_clock_transport = (2|lambda_D|/Z_min)||R_Q||E_transport
B_readout_clock = 0
=> D_tau ln alpha_EM = 0.
```

This means we do **not** have to pretend local time is silent. If the local EM residual branch is exactly on the root, the clock alpha drift dies because the source amplitude is zero, not because `tau_clock_time` was smuggled to zero.

## Source Register
{table(data["sources"])}

## Tau Zero / Exact Root Certificate
{table(data["zeros"])}

## Dynamic Clock Finite Source Rows
{table(data["finite"])}

## Firewalls
{table(data["firewalls"])}

## Decision
{table(data["decision"])}

## Status
{table(data["status"])}

## Next Target
{table(data["next"])}
""",
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(
        f"""# 726 - PPC4161 Tau Clock Zero Certificate Or Dynamic Clock Source Row

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Clock-scored alpha drift finite branch:

```text
|D_tau ln alpha_EM| <= C_D |Delta m tau_clock_time| + E_HO + E_clock_transport + B_readout_clock.
```

Direct tau-zero sufficient condition:

```text
chi_X=chi_bar(q_obs(Phi),theta_fixed), Dq_obs[T_clock]=0
=> tau_clock_time = 0.
```

Exact-root bypass:

```text
R_Q=0, Delta m=0,
Z_A=Z_*+lambda_D <R_Q,R_Q>_P with no linear residual term,
E_clock_transport=(2|lambda_D|/Z_min)||R_Q||E_transport,
B_readout_clock=0
=> D_tau ln alpha_EM=0.
```

Interpretation: the clean local route is to prove exact local residual root and no-linear EM kinetic ownership. It is stronger than assuming the clock-time projection vanishes.
""",
        encoding="utf-8",
    )


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(claims[0].keys()) if claims else [
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
        "title",
        "notes",
    ]
    claim_row = {field: "" for field in fieldnames}
    claim_row.update(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_empirical_interface",
            "claim": "4710 derives a direct tau-zero sufficient condition and a stronger exact-root bypass for clock alpha drift without assuming tau_clock_time=0.",
            "current_evidence": "Generated source register, tau-zero/exact-root certificate rows, finite dynamic source rows, firewalls, decision, status, next target and validation.",
            "status": "exact_root_bypass_conditional_clock_alpha_zero_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Claiming local clock pass before R_Q=0/no-linear EM kinetic owner is parent-certified, or splitting product factors without source rows.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Tau clock zero certificate or dynamic clock source row",
            "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
        }
    )
    existing = next((row for row in claims if row.get("claim_id") == CLAIM_ID), None)
    if existing is None:
        claims.append(claim_row)
    else:
        existing.update(claim_row)
    write_csv(CLAIMS_PATH, claims)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: direct `tau_clock_time=0` is only a sufficient condition, but the better branch is now derived: exact local residual root `R_Q=0` plus no-linear EM kinetic owner gives `D_tau ln alpha_EM=0` without assuming tau silence.
- Finite row: `|D_tau ln alpha_EM| <= C_D |Delta m tau_clock_time| + E_HO + E_clock_transport + B_readout_clock`.
- Firewall: exact-root bypass is not a clock/local-GR claim until `R_Q=0` and the no-linear kinetic owner are parent-certified.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: turns the clock/tau obstruction into an exact-root bypass theorem plus finite dynamic source-row formula.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: 2026-07-07

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4710-Y5-R2FR-tau-clock-zero-certificate-or-dynamic-clock-source-row.md`

## What Changed

Direct tau silence is only a sufficient condition:

```text
chi_X=chi_bar(q_obs), Dq_obs[T_clock]=0
=> tau_clock_time=0.
```

The stronger move is the exact-root bypass:

```text
R_Q=0, Delta m=0, no linear EM kinetic owner,
E_clock_transport=(2|lambda_D|/Z_min)||R_Q||E_transport,
B_readout_clock=0
=> D_tau ln alpha_EM=0.
```

This avoids smuggling in `tau_clock_time=0`; the local clock residual vanishes because the source amplitude is zero.

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not claim tau silence unless `chi_X` is parent-owned q-basic/stationary.
- Do not claim exact-root clock pass until `R_Q=0` and no-linear EM kinetic owner are parent-certified.
- Do not push to GitHub unless Martin explicitly asks for a GitHub update.
""",
        encoding="utf-8",
    )


def validation_rows(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL4710_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4710_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4710_2_direct_tau_zero", any(row["certificate_id"] == "TZC4710_0_direct_tau_zero_sufficient_condition" for row in data["zeros"]), "direct tau-zero sufficient condition present")
    add("VAL4710_3_exact_root_bypass", any(row["certificate_id"] == "TZC4710_1_exact_root_bypass" for row in data["zeros"]), "exact-root bypass theorem present")
    add("VAL4710_4_transport_root_zero", any(row["certificate_id"] == "TZC4710_3_transport_root_zero" for row in data["zeros"]), "transport root-zero theorem present")
    add("VAL4710_5_finite_formula", any("C_D |Delta m tau_clock_time|" in row["formula"] for row in data["finite"]), "finite dynamic clock formula present")
    add("VAL4710_6_clock_gate", any(row["value_or_bound"] == "2.1e-18" for row in data["finite"]), "2.1e-18 yr^-1 clock pressure gate retained")
    add("VAL4710_7_firewalls", len(data["firewalls"]) >= 3, "firewalls present")
    add("VAL4710_8_next_target", data["next"][0]["target"] == NEXT_TARGET, "4711 next target selected")
    add("VAL4710_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4710_10_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4710_11_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4710_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4710_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")
    add("VAL4710_14_resume_updated", NEXT_TARGET in text(RESUME_PATH), "resume bookmark updated")

    for csv_path in [
        SOURCE_REGISTER,
        ZERO_CSV,
        FINITE_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4710_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4710_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [
        data["zeros"],
        data["finite"],
        data["firewalls"],
        data["decision"],
        data["status"],
        data["next"],
    ]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4710_15_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4710_16_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4710_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_status_next(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "zeros": zero_rows(timestamp),
        "finite": finite_rows(timestamp),
        "firewalls": firewall_rows(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(ZERO_CSV, data["zeros"])
    write_csv(FINITE_CSV, data["finite"])
    write_csv(FIREWALL_CSV, data["firewalls"])
    write_csv(DECISION_CSV, data["decision"])
    write_csv(STATUS_CSV, data["status"])
    write_csv(NEXT_CSV, data["next"])

    write_documents(timestamp, data)
    update_registers(timestamp)
    validation = validation_rows(timestamp, data)
    write_csv(VALIDATION_CSV, validation)

    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
