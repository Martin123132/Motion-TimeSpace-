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

CHECKPOINT = "4709"
CLAIM_ID = "L-551"
MARKER = "PPC4161_CLOCK_READOUT_TAU_MAP_OR_BREADOUT_FIRST_SOURCE_ROW_4709"
PACKET_MARKER = "PPC4161_PACKET_CLOCK_READOUT_TAU_MAP_OR_BREADOUT_FIRST_SOURCE_ROW_4709"
DECISION = "CLOCK_TAU_MAP_EXACT_CONDITIONAL_PRODUCT_ONLY_BREADOUT_ROW_RETAINED_NONCLAIM"
NEXT_TARGET = "4710-Y5-R2FR-tau-clock-zero-certificate-or-dynamic-clock-source-row.md"

DOC_PATH = POST / "4709-Y5-R2FR-clock-readout-tau-map-or-Breadout-first-source-row.md"
FORMAL_PATH = FORMAL / "725-PPC4161-clock-readout-tau-map-or-Breadout-first-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4708_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4708_NEXT_TARGET.csv"
CSV_4708_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4708_BRAD_BREADOUT_SOURCE_ROWS_NONCLAIM.csv"
CSV_4708_TRANSFER = SOURCE_DIR / "P8_Y5_R2FR_4708_CLOCK_R10_TRANSFER_FIREWALL_ROWS.csv"
CSV_4708_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4708_VALIDATION.csv"
CSV_4325_TAU = SOURCE_DIR / "P8_Y5_R2FR_4325_TAU_LOCK_AUDIT.csv"
CSV_4325_CLOCK_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4325_CLOCK_TAIL_LEDGER.csv"
CSV_4660_OBS = SOURCE_DIR / "P8_Y5_R2FR_4660_OBSERVED_COFRAME_CLOCK_ZERO_IMPORT.csv"
CSV_4660_NORMAL = SOURCE_DIR / "P8_Y5_R2FR_4660_BCLOCK_MEMORY_NORMAL_FORM.csv"
CSV_4660_DYN = SOURCE_DIR / "P8_Y5_R2FR_4660_DYNAMIC_CLOCK_REDSHIFT_BOUND_ROWS.csv"
CSV_4660_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4660_VALIDATION.csv"
CSV_1051_CLOCK = SOURCE_DIR / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv"
CSV_1052_TAU = SOURCE_DIR / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv"
CSV_1052_CLOCK = SOURCE_DIR / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
CSV_1052_R10 = SOURCE_DIR / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4709_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4709_CLOCK_TAU_MAP_THEOREM_ROWS.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4709_CLOCK_PRODUCT_ISOLATION_ROWS.csv"
BREADOUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4709_DYNAMIC_BREADOUT_SOURCE_ROW_TEMPLATE.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4709_TRANSFER_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4709_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4709_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4709_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4709_VALIDATION.csv"


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
        ("SRC4709_00_4708_next", CSV_4708_NEXT, "NT4708_0", "4708 handoff to clock tau/readout target"),
        ("SRC4709_01_4708_clock_product", CSV_4708_TAIL, "TAIL4708_2_clock_product", "4708 product-only clock handle"),
        ("SRC4709_02_4708_R10_firewall", CSV_4708_TRANSFER, "FW4708_0_no_clock_to_R10", "4708 clock-to-R10 transfer firewall"),
        ("SRC4709_03_4708_validation", CSV_4708_VALIDATION, "VAL4708_OVERALL", "4708 validation"),
        ("SRC4709_04_4325_single_tau", CSV_4325_TAU, "AUD4325_0_single_tau", "4325 single parent tau audit"),
        ("SRC4709_05_4325_surface_coframe", CSV_4325_TAU, "AUD4325_1_surface_coframe", "4325 observed coframe/tau audit"),
        ("SRC4709_06_4325_Hperp_zero", CSV_4325_TAU, "AUD4325_3_Hperp_zero", "4325 conditional tau Hperp zero"),
        ("SRC4709_07_4325_clock_tail", CSV_4325_CLOCK_TAIL, "CT4325_3_clock", "4325 clock readout residual tail"),
        ("SRC4709_08_4660_clock_matter", CSV_4660_OBS, "BCZ4660_1_clock_matter", "4660 local Lorentz/eikonal clock matter"),
        ("SRC4709_09_4660_same_tau", CSV_4660_OBS, "BCZ4660_4_same_tau_role", "4660 same observed tau role"),
        ("SRC4709_10_4660_clock_zero_result", CSV_4660_OBS, "BCZ4660_5_result", "4660 fixed coframe clock zero"),
        ("SRC4709_11_4660_observed_functional", CSV_4660_NORMAL, "BCN4660_2_observed_coframe_functional", "4660 observed proper-time functional"),
        ("SRC4709_12_4660_residual_vector", CSV_4660_NORMAL, "BCN4660_3_residual_vector", "4660 dynamic clock residual vector"),
        ("SRC4709_13_4660_product_bound", CSV_4660_DYN, "BCB4660_1_clock_product_1sigma", "4660 best clock product pressure gate"),
        ("SRC4709_14_4660_Xi_identity", CSV_4660_DYN, "BCB4660_4_Xi_identity", "4660 Xi clock product identity"),
        ("SRC4709_15_4660_validation", CSV_4660_VALIDATION, "VAL4660_OVERALL", "4660 validation"),
        ("SRC4709_16_1051_best_clock", CSV_1051_CLOCK, "BAP1051_2_best_current_product", "1051 best current clock product"),
        ("SRC4709_17_1052_tau_verdict", CSV_1052_TAU, "TCN1052_4_verdict", "1052 standalone alpha from clocks fails"),
        ("SRC4709_18_1052_clock_product", CSV_1052_CLOCK, "ACB1052_2", "1052 best clock product row"),
        ("SRC4709_19_1052_R10_transfer", CSV_1052_R10, "RAP1052_2_clock_to_R10_transfer", "1052 clock-to-R10 transfer block"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CTM4709_0_observed_coframe_tau_zero",
            "claim_piece": "D_v d_tau_clk zero",
            "formal_statement": "If e_obs=e_bar(q_obs(Phi)), g_obs=e_obs^T eta e_obs, Dq_obs[v]=0, c and standards are fixed, and clock matter is local Lorentz/eikonal matter coupled only to e_obs, then D_v g_obs=0 and D_v d_tau_clk=0 for d_tau_clk=sqrt(-g_obs(dx,dx))/c.",
            "proof": "The vertical derivative reaches the clock through e_obs(q_obs) only. The chain rule gives D_v e_obs=(De_bar)Dq_obs[v]=0; hence D_v g_obs=0 and the proper-time integrand has zero vertical derivative.",
            "uses_sources": "BCZ4660_0_observed_coframe;BCZ4660_1_clock_matter;BCN4660_2_observed_coframe_functional",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PARENT_SIGNATURE_NEEDED",
            "failure_mode": "shadow coframe, nonminimal clock-flow coupling, variable standards, or detector readout not factoring through q_obs",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CTM4709_1_observed_readout_frequency_zero",
            "claim_piece": "D_v ln nu_obs zero",
            "formal_statement": "If nu_A^obs=R_A(q_obs(Phi), Zbar(q_obs), theta_A, standards) and theta_A/standards are representation-fixed or q-basic, then D_v ln(nu_A^obs/nu_B^obs)=0 for all v in ker(Dq_obs).",
            "proof": "Both transition frequencies are quotient functions. All vertical derivatives enter through Dq_obs[v] or fixed constants; the sensitivity decomposition has no residual rho_clock_readout slot on this branch.",
            "uses_sources": "BCZ4660_2_fixed_constants;BCZ4660_3_no_clock_specific_slot;BCN4660_1_sensitivity_decomposition",
            "current_status": "EXACT_CONDITIONAL_THEOREM_READOUT_SIGNATURE_NEEDED",
            "failure_mode": "rho_clock_readout, epsilon_nonminimal_clock or an apparatus/material map with hidden representative dependence",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CTM4709_2_single_tau_role_lock",
            "claim_piece": "tau split zero",
            "formal_statement": "If tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout on a preselected parent branch, then the clock time projection cannot be separately fitted after variation; epsilon_tau_role=0 and tau split residuals are not allowed to absorb local failures.",
            "proof": "4325 supplies the single-parent-time branch. The same tau role used by clocks, sources and orbital/PPN readouts prevents switching the readout clock after seeing the residual vector.",
            "uses_sources": "AUD4325_0_single_tau;AUD4325_2_reference_no_fit;BCZ4660_4_same_tau_role",
            "current_status": "EXACT_CONDITIONAL_BRANCH_LOCK",
            "failure_mode": "post-fit reference selection or separate tau maps for clocks versus source/test systems",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CTM4709_3_clock_Breadout_zero_branch",
            "claim_piece": "B_readout_clock zero",
            "formal_statement": "On CTM4709_0-2 plus the 4708 observed readout functor branch, the clock-sector readout tail obeys B_readout_clock=0. This does not by itself zero the R10, WEP, material or orbital readout tails.",
            "proof": "Substitute D_v d_tau_clk=0, D_v ln nu_obs=0 and epsilon_tau_role=0 into the 4660 normal form for b_clock_mem and the 4708 definition of B_readout.",
            "uses_sources": "TAIL4708_1_Breadout;BCZ4660_5_result;BCN4660_3_residual_vector",
            "current_status": "EXACT_CONDITIONAL_CLOCK_SECTOR_ONLY",
            "failure_mode": "using clock zero as a universal readout zero without arena-specific maps",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def product_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CPI4709_0_product_bound_law",
            "quantity": "B_readout*tau_clock_time",
            "law": "|B_readout*tau_clock_time| <= 2.1e-18 yr^-1 on the imported best clock product row, modulo the same branch-identification assumptions.",
            "what_it_does": "gives a real pressure gate for the product",
            "what_it_does_not_do": "does not isolate standalone B_readout",
            "needed_to_isolate": "nonzero lower bound or normalization for tau_clock_time plus signed chi_X/Xhat parent map",
            "source_rows": "TAIL4708_2_clock_product;BCB4660_1_clock_product_1sigma;BAP1051_2_best_current_product;ACB1052_2",
            "status": "SOURCE_BACKED_PRODUCT_ONLY_NOT_STANDALONE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CPI4709_1_Xi_identity",
            "quantity": "Xi_clock",
            "law": "Xi_clock=C_D |Delta m tau_clock_time|",
            "what_it_does": "separates clock product pressure into sensitivity, memory amplitude and clock-time projection if each term is parent-owned",
            "what_it_does_not_do": "does not permit setting C_D, Delta m or tau_clock_time to one",
            "needed_to_isolate": "source-backed C_D, Delta m and tau_clock_time rows, or a theorem zeroing one factor",
            "source_rows": "BCB4660_4_Xi_identity;TCN1052_0_product_definition;TCN1052_4_verdict",
            "status": "CONDITIONAL_PRODUCT_IDENTITY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CPI4709_2_redshift_anchor",
            "quantity": "alpha_clock_redshift",
            "law": "alpha_clock_redshift <= 2.48e-05 constrains the full clock/readout residual vector, not B_readout alone.",
            "what_it_does": "provides an independent LPI/redshift anchor for a future dynamic clock source row",
            "what_it_does_not_do": "does not split metric, clock, transport and readout residuals",
            "needed_to_isolate": "local potential/source normalization and clock readout map",
            "source_rows": "BCB4660_3_redshift_anchor;BCN4660_4_redshift_projection",
            "status": "ANCHOR_AVAILABLE_PROJECTION_MISSING_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def breadout_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BRS4709_0_exact_clock_zero_candidate",
            "branch": "fixed_observed_coframe_clock_branch",
            "component": "B_readout_clock",
            "formula": "B_readout_clock=0 if e_obs=e_bar(q_obs), clock matter/readout are quotient-owned, constants are q-basic/fixed, and tau roles are single-branch",
            "numeric_value": "",
            "units": "dimensionless_or_fractional_rate",
            "source_path": f"{CSV_4660_OBS};{CSV_4325_TAU};{CSV_4708_TAIL}",
            "missing_before_claim": "parent signature that clock readout functor and standards are quotient-owned in the final action",
            "status": "EXACT_CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BRS4709_1_best_clock_product_row",
            "branch": "dynamic_clock_product_branch",
            "component": "B_readout_tau_clock_time",
            "formula": "|B_readout*tau_clock_time| <= 2.1e-18 yr^-1",
            "numeric_value": "2.1e-18",
            "units": "yr^-1",
            "source_path": f"{CSV_4660_DYN};{CSV_1051_CLOCK};{CSV_1052_CLOCK}",
            "missing_before_claim": "tau_clock_time normalization, chi_X/Xhat parent map and split of E_HO/E_transport from B_readout",
            "status": "SOURCE_BACKED_PRODUCT_ONLY_NOT_STANDALONE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BRS4709_2_dynamic_clock_source_contract",
            "branch": "finite_dynamic_clock_branch",
            "component": "b_clock_mem_abs",
            "formula": "|rho_clock_readout|+|epsilon_nonminimal_clock|+|epsilon_tau_role|+|Xi_clock|+|E_HO|+|E_transport|",
            "numeric_value": "",
            "units": "declared per source row",
            "source_path": str(CSV_4660_DYN),
            "missing_before_claim": "rho_clock_readout;epsilon_nonminimal_clock;epsilon_tau_role;Xi_clock;E_HO;E_transport values and source paths",
            "status": "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BRS4709_3_R10_transfer_block",
            "branch": "clock_to_R10_transfer",
            "component": "B_readout_R10_transfer",
            "formula": "alpha_R10_readout(lambda) requires K_R10_EM(lambda), tau_R10, material profile and source/test charges",
            "numeric_value": "",
            "units": "arena_specific",
            "source_path": f"{CSV_4708_TRANSFER};{CSV_1052_R10}",
            "missing_before_claim": "K_R10_EM(lambda);tau_R10;source/test charge maps;material response maps",
            "status": "TRANSFER_BLOCKED_MAPS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4709_0_no_clock_product_to_Breadout",
            "rule": "A bound on B_readout*tau_clock_time is not a bound on B_readout unless tau_clock_time has a parent-owned nonzero normalization.",
            "evidence": "TCN1052_4_verdict;CPI4709_0_product_bound_law",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4709_1_no_clock_zero_to_all_readouts",
            "rule": "The observed-coframe clock zero branch is clock-sector only; it does not automatically prove R10, WEP, material, PPN or orbital readout tails are zero.",
            "evidence": "CTM4709_3_clock_Breadout_zero_branch;FW4708_0_no_clock_to_R10",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4709_2_no_tau_refit",
            "rule": "The tau/reference map must be selected before residual comparison; fitting it after seeing clock, orbital, R10 or PPN residuals is scored as a residual, not erased.",
            "evidence": "AUD4325_2_reference_no_fit;CTM4709_2_single_tau_role_lock",
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
            "branch": "MTS_R2FR_Y5_CLOCK_TAU_MAP_4709",
            "decision": DECISION,
            "reason": "The clock proper-time/readout zero can be derived on the fixed observed-coframe branch, but empirical clock data remain product-only unless tau_clock_time/chi_X normalization or dynamic source rows are supplied.",
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
            "derived": "conditional D_v d_tau_clk=0; conditional D_v ln nu_obs=0; single-tau role lock; clock-sector B_readout zero branch",
            "not_derived": "standalone B_readout value; tau_clock_time normalization; chi_X/Xhat parent map; R10/WEP/material transfer maps; dynamic clock residual components",
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
            "next_id": "NT4709_0",
            "target": NEXT_TARGET,
            "reason": "4709 gives the exact clock-sector zero branch and the product-only empirical row; 4710 must either parent-sign tau_clock_time/chi_X zero or fill the dynamic clock source row with real components.",
            "derive_first": "prove tau_clock_time=0 or fixed quotient clock readout from the final parent action",
            "fallback": "fill BRS4709_2 dynamic source row and keep product-only nonclaim status",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4709 - Clock Readout Tau Map Or B_readout First Source Row

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
4709 stops the clock/readout branch from floating.

Exact clock-sector route:

```text
e_obs = e_bar(q_obs(Phi))
Dq_obs[v] = 0
clock matter/readout = quotient-owned local Lorentz/eikonal branch
fixed q-basic standards and one parent tau role
=> D_v g_obs = 0
=> D_v d_tau_clk = 0
=> D_v ln(nu_A^obs/nu_B^obs) = 0
=> B_readout_clock = 0.
```

This is a real conditional derivation, not a fitted closure. It is also deliberately narrow: it only zeros the clock-sector readout tail on the fixed observed-coframe branch.

Empirical clock evidence remains product-only:

```text
|B_readout * tau_clock_time| <= 2.1e-18 yr^-1.
```

That row cannot become a standalone `B_readout` bound until `tau_clock_time`, `chi_X/Xhat` normalization, and higher-order/transport split rows are parent-owned or source-backed.

## Source Register
{table(data["sources"])}

## Clock Tau Map Theorem Rows
{table(data["theorems"])}

## Product-Isolation Rows
{table(data["products"])}

## Dynamic B_readout Source Row Template
{table(data["breadout"])}

## Transfer Firewalls
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
        f"""# 725 - PPC4161 Clock Readout Tau Map Or B_readout First Source Row

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Let `v in ker(Dq_obs)` and let the clock branch be:

```text
e_obs = e_bar(q_obs(Phi)),
g_obs = e_obs^T eta e_obs,
d_tau_clk = sqrt(-g_obs(dx,dx))/c,
nu_A^obs = R_A(q_obs(Phi), Zbar(q_obs), theta_A, standards).
```

If `theta_A` and standards are fixed or q-basic, then:

```text
D_v e_obs = 0
D_v g_obs = 0
D_v d_tau_clk = 0
D_v ln(nu_A^obs/nu_B^obs) = 0.
```

Therefore the fixed observed-coframe clock-sector branch gives:

```text
B_readout_clock = 0.
```

The finite empirical branch remains:

```text
|B_readout * tau_clock_time| <= 2.1e-18 yr^-1
```

and is product-only. No standalone `B_readout`, R10, WEP, PPN, material or orbital transfer is allowed without the relevant tau/source/readout maps.
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
            "claim": "4709 derives the conditional clock-sector tau/readout zero branch and stages the first B_readout product/source-row firewall.",
            "current_evidence": "Generated source register, clock tau-map theorem rows, product-isolation rows, dynamic B_readout source-row template, firewalls, decision, status, next target and validation.",
            "status": "clock_tau_map_conditional_zero_product_only_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Promoting clock product evidence to standalone B_readout or transferring clock zero to R10/WEP without arena maps.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Clock readout tau map or B_readout first source row",
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
- Movement: the fixed observed-coframe clock branch now has a precise conditional zero: `D_v d_tau_clk=0`, `D_v ln(nu_A^obs/nu_B^obs)=0`, hence `B_readout_clock=0`.
- Empirical row: `|B_readout*tau_clock_time| <= 2.1e-18 yr^-1` remains product-only.
- Firewall: no standalone `B_readout` and no R10/WEP/PPN/material/orbital transfer without tau/source/readout maps.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: clock-sector tau/readout exact-zero branch plus product-only B_readout source-row gate.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: 2026-07-07

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4709-Y5-R2FR-clock-readout-tau-map-or-Breadout-first-source-row.md`

## What Changed

The clock-sector tau/readout map now has a precise fixed-branch theorem:

```text
e_obs=e_bar(q_obs), Dq_obs[v]=0, fixed q-basic standards
=> D_v d_tau_clk = 0
=> D_v ln(nu_A^obs/nu_B^obs) = 0
=> B_readout_clock = 0.
```

The empirical clock row is still only:

```text
|B_readout * tau_clock_time| <= 2.1e-18 yr^-1.
```

It cannot be used as standalone `B_readout` without a parent-owned `tau_clock_time` / `chi_X` normalization or a filled dynamic clock source row.

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not use clock product rows as standalone `B_readout`.
- Do not transfer clock-sector zero to R10/WEP/PPN/material/orbital arenas without arena maps.
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

    add("VAL4709_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4709_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4709_2_tau_zero", any(row["claim_piece"] == "D_v d_tau_clk zero" for row in data["theorems"]), "D_v d_tau_clk zero theorem row present")
    add("VAL4709_3_frequency_zero", any(row["claim_piece"] == "D_v ln nu_obs zero" for row in data["theorems"]), "D_v ln nu_obs zero theorem row present")
    add("VAL4709_4_single_tau", any(row["claim_piece"] == "tau split zero" for row in data["theorems"]), "single tau role lock present")
    add("VAL4709_5_clock_only_zero", any(row["claim_piece"] == "B_readout_clock zero" for row in data["theorems"]), "clock-sector B_readout zero branch present")
    add("VAL4709_6_product_only", any(row["status"] == "SOURCE_BACKED_PRODUCT_ONLY_NOT_STANDALONE" for row in data["products"] + data["breadout"]), "clock product-only row present")
    add("VAL4709_7_dynamic_template", any(row["row_id"] == "BRS4709_2_dynamic_clock_source_contract" for row in data["breadout"]), "dynamic source-row template present")
    add("VAL4709_8_R10_firewall", any(row["firewall_id"] == "FW4709_1_no_clock_zero_to_all_readouts" for row in data["firewalls"]), "cross-arena transfer firewall present")
    add("VAL4709_9_next_target", data["next"][0]["target"] == NEXT_TARGET, "4710 next target selected")
    add("VAL4709_10_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4709_11_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4709_12_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4709_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4709_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")
    add("VAL4709_15_resume_updated", NEXT_TARGET in text(RESUME_PATH), "resume bookmark updated")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        PRODUCT_CSV,
        BREADOUT_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4709_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4709_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [
        data["theorems"],
        data["products"],
        data["breadout"],
        data["firewalls"],
        data["decision"],
        data["status"],
        data["next"],
    ]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4709_16_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    forbidden_promotions = [
        row for row in data["breadout"] + data["products"]
        if str(row.get("status", "")).endswith("STANDALONE") and str(row.get("valid_for_claim", "")).lower() == "true"
    ]
    add("VAL4709_17_no_standalone_Breadout", not forbidden_promotions, "no standalone B_readout claim is promoted")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4709_18_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4709_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_status_next(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "products": product_rows(timestamp),
        "breadout": breadout_rows(timestamp),
        "firewalls": firewall_rows(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorems"])
    write_csv(PRODUCT_CSV, data["products"])
    write_csv(BREADOUT_CSV, data["breadout"])
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
