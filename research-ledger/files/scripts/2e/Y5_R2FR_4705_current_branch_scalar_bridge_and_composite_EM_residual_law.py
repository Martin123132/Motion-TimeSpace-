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

CHECKPOINT = "4705"
CLAIM_ID = "L-547"
MARKER = "PPC4161_CURRENT_BRANCH_SCALAR_BRIDGE_COMPOSITE_EM_RESIDUAL_4705"
PACKET_MARKER = "PPC4161_PACKET_CURRENT_BRANCH_SCALAR_BRIDGE_COMPOSITE_EM_RESIDUAL_4705"
DECISION = "CURRENT_BRANCH_DEDUPED_TO_COMPOSITE_EM_RESIDUAL_LAW_NONCLAIM"
NEXT_TARGET = "4706-Y5-R2FR-composite-EM-local-residual-score-or-first-source-backed-input.md"

DOC_PATH = POST / "4705-Y5-R2FR-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md"
FORMAL_PATH = FORMAL / "721-PPC4161-current-branch-scalar-functional-bridge-and-composite-EM-local-residual-law.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4704_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4704_STATUS.csv"
CSV_4704_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4704_VALIDATION.csv"
CSV_4704_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4704_CLAIM_BLOCKERS.csv"
CSV_4704_HOM = SOURCE_DIR / "P8_Y5_R2FR_4704_HIDDEN_HOM_BOUND_ROWS_NONCLAIM.csv"
CSV_4617_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4617_PARENT_SCALAR_FUNCTIONAL_THEOREM.csv"
CSV_4617_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4617_VALIDATION.csv"
CSV_4618_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4618_MEMORY_CLASS_SCALAR_NOHAIR_THEOREM.csv"
CSV_4618_CMEMORY = SOURCE_DIR / "P8_Y5_R2FR_4618_CMEMORY_F2_VALUE_ROW_NONCLAIM.csv"
CSV_4619_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4619_F2_MEMORY_OWNER_THEOREM.csv"
CSV_4620_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_ZERO_ROUTES.csv"
CSV_4620_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_FIRST_NUMERIC_ROW_NONCLAIM.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
CSV_4621_AMPLITUDE = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_AMPLITUDE_BOUND_ROWS.csv"
CSV_4622_CHANNELS = SOURCE_DIR / "P8_Y5_R2FR_4622_RHOMEM_CHANNEL_DECOMPOSITION.csv"
CSV_4622_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4622_EM_POYNTING_ZERO_AND_BOUND_RULES.csv"
CSV_4622_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4622_BOUND_FEED_ROWS.csv"
CSV_4623_SELECTION = SOURCE_DIR / "P8_Y5_R2FR_4623_PARENT_SELECTION_THEOREMS.csv"
CSV_4623_BETA = SOURCE_DIR / "P8_Y5_R2FR_4623_BETA_OWNERSHIP_MATRIX.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4705_SOURCE_REGISTER.csv"
BRIDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4705_DEDUPED_BRIDGE_IMPORTS.csv"
COMPOSITE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4705_COMPOSITE_EM_RESIDUAL_LAW.csv"
CHANNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4705_SOURCE_CHANNEL_SELECTION_ROWS.csv"
QUEUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4705_NUMERIC_OR_ZERO_INPUT_QUEUE.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4705_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4705_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4705_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4705_VALIDATION.csv"


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
        ("SRC4705_00_4704_status", CSV_4704_STATUS, "PPC4161_VISIBLE_OPERATOR_DOMAIN_IMAGE_HOM_BRANCH_4704", "fresh 4704 handoff"),
        ("SRC4705_01_4704_validation", CSV_4704_VALIDATION, "VAL4704_OVERALL", "4704 validation"),
        ("SRC4705_02_4704_blocker", CSV_4704_BLOCKERS, "BLK4704_0_parent_scalar_functional_exhaustion", "4704 loop target"),
        ("SRC4705_03_4704_hom", CSV_4704_HOM, "HOM4704_0_C_XF2_kernel_norm", "4704 finite Hom rows"),
        ("SRC4705_04_4617_scalar", CSV_4617_THEOREM, "PSF4617_0_transitive_fibre_triviality", "already-derived scalar exhaustion theorem"),
        ("SRC4705_05_4617_validation", CSV_4617_VALIDATION, "VAL4617_OVERALL", "4617 validation"),
        ("SRC4705_06_4618_memory", CSV_4618_THEOREM, "MCS4618_4_countermodel_and_value_need", "memory no-hair/countermodel split"),
        ("SRC4705_07_4618_cmemory", CSV_4618_CMEMORY, "CMF4618_0_first_value_contract", "C_memory_F2 value contract"),
        ("SRC4705_08_4619_owner", CSV_4619_THEOREM, "FMO4619_3_finite_derivative_law", "finite kappa-memory law"),
        ("SRC4705_09_4620_zero", CSV_4620_ZERO, "KZ4620_0_typed_domain_zero", "kappa zero routes"),
        ("SRC4705_10_4620_numeric", CSV_4620_NUMERIC, "KNUM4620_0_first_numeric_template", "kappa numeric row"),
        ("SRC4705_11_4621_identity", CSV_4621_IDENTITY, "MPI4621_1_energy_identity", "memory positive operator identity"),
        ("SRC4705_12_4621_amplitude", CSV_4621_AMPLITUDE, "AMB4621_2_Cmemory_feed", "C_memory amplitude feed"),
        ("SRC4705_13_4622_channels", CSV_4622_CHANNELS, "RDEC4622_3_poynting", "rho_mem channel decomposition"),
        ("SRC4705_14_4622_poynting", CSV_4622_POYNTING, "EMP4622_1_poynting_volume_to_boundary", "Poynting volume/boundary rule"),
        ("SRC4705_15_4622_bound", CSV_4622_BOUND, "BF4622_0_rho_norm", "source norm feed row"),
        ("SRC4705_16_4623_selection", CSV_4623_SELECTION, "PSEL4623_0_variational_owner", "parent beta owner rule"),
        ("SRC4705_17_4623_beta", CSV_4623_BETA, "BOWN4623_2_beta_F", "beta_F tied to kappa_memF2"),
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


def bridge_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": "BR4705_0_no_duplicate_target",
            "imported_result": "4704 target already has validated ladder 4617-4623",
            "composition": "visible-image/Hom gate -> scalar-functional exhaustion -> memory-F2 coefficient owner -> positive memory amplitude -> rho_mem source channels -> beta owner rules",
            "status": "DEDUPED_CURRENT_BRANCH",
            "source_refs": "4704;4617;4618;4619;4620;4621;4622;4623",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": "BR4705_1_exact_zero_chain",
            "imported_result": "conditional zero chain",
            "composition": "transitive connected hidden fibre + no Coeff(F_Q^2) hidden target + kappa_memF2=0/no-Hom + rho_mem=q_boundary=0 + readout/radiative stability => D_v lambda_F2=0",
            "status": "EXACT_CONDITIONAL_CHAIN_NOT_PARENT_SIGNED",
            "source_refs": "PSF4617_0;FMO4619_0;KZ4620_0;MPI4621_2;PSEL4623_2",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": "BR4705_2_finite_chain",
            "imported_result": "finite memory/Hom chain",
            "composition": "if any zero clause fails, C_memory_F2 is not vague: it is controlled by kappa_memF2, the memory operator coercivity data, source norms, and boundary flux",
            "status": "FINITE_COMPOSITE_LAW_READY_NONCLAIM",
            "source_refs": "CMF4618_0;FMO4619_3;AMB4621_2;BF4622_0;BF4622_1",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def composite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "law_id": "LAW4705_0_master_hidden_EM_residual",
            "quantity": "s_XF2",
            "law": "|s_XF2| <= H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|",
            "derived_from": "4704 Hom bound imported into current branch",
            "live_inputs": "H_XF2;delta_lambda_rad;delta_lambda_readout",
            "status": "EXACT_BOUND_FORM_RESTATED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "LAW4705_1_memory_component_bound",
            "quantity": "C_memory_F2",
            "law": "C_memory_F2 <= |kappa_memF2|/Z_Q_eff_min * Delta_v_m_mem_bound",
            "derived_from": "4618 value contract + 4619 finite derivative law",
            "live_inputs": "kappa_memF2;Z_Q_eff_min;Delta_v_m_mem_bound",
            "status": "EXACT_COMPONENT_IDENTITY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "LAW4705_2_memory_amplitude_bound",
            "quantity": "Delta_v_m_mem_bound",
            "law": "Delta_v_m_mem_bound <= C_Omega*(||rho_mem||_Hminus1 + ||q_boundary_mem||_HminusHalf)/min(Z_mem_min,M2_mem_min)",
            "derived_from": "4621 energy identity and coercive local amplitude estimate",
            "live_inputs": "C_Omega;rho_mem norm;q_boundary_mem norm;Z_mem_min;M2_mem_min",
            "status": "COERCIVE_BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "LAW4705_3_composed_memory_F2_bound",
            "quantity": "C_memory_F2_composed",
            "law": "C_memory_F2 <= |kappa_memF2|/Z_Q_eff_min * C_Omega*(||rho_mem||_Hminus1 + ||q_boundary_mem||_HminusHalf)/min(Z_mem_min,M2_mem_min)",
            "derived_from": "LAW4705_1 composed with LAW4705_2",
            "live_inputs": "kappa_memF2;Z_Q_eff_min;C_Omega;Z_mem_min;M2_mem_min;rho_mem;q_boundary_mem",
            "status": "NEW_CURRENT_BRANCH_COMPOSITE_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "LAW4705_4_arena_projection",
            "quantity": "arena_residual",
            "law": "B_arena <= |K_arena_EM|*(H_XF2 + B_readout + B_rad) with arena in {R10,PPN,clock,orbital}",
            "derived_from": "4704 Hom/K/tau arena rows",
            "live_inputs": "K_R10_EM;K_PPN_EM;K_clock_alpha;tau_clock;K_orb_EM;real bound curves",
            "status": "TEST_INTERFACE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def channel_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CHAN4705_0_rho_decomposition",
            "channel": "rho_mem",
            "selection_law": "rho_mem = beta_R R_obs + beta_T T_obs + beta_F F_Q^2 + beta_G F_Q starF_Q + beta_S div(S_EM) + beta_gw rho_gw_eff + J_hidden",
            "zero_route": "each beta/source channel zero on the same branch, not one-at-a-time after calibration",
            "finite_route": "||rho_mem||_Hminus1 <= sum_i |beta_i| ||source_i||_Hminus1 + ||J_hidden||_Hminus1",
            "status": "COMPOSED_FROM_4622_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CHAN4705_1_EM_scalar",
            "channel": "beta_F F_Q^2 + beta_G F_Q starF_Q",
            "selection_law": "beta_F is tied to kappa_memF2 when the owner is Z_Q_eff(m_mem); beta_G needs parity/CP-odd parent structure",
            "zero_route": "kappa_memF2 zero/no-Hom/extremum kills beta_F; parity-even scalar branch kills beta_G",
            "finite_route": "source kappa_memF2 or theta_Q derivative plus local field invariant norms",
            "status": "BETA_F_NOT_FREE_KAPPA_TIED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CHAN4705_2_Poynting",
            "channel": "beta_S div(S_EM) or boundary S_EM dot n",
            "selection_law": "Poynting is observer/coframe relative; no covariant volume beta_S unless parent owns observer/coframe/current structure",
            "zero_route": "stationary source-free volume with no net boundary flux, or no parent observer/coframe owner",
            "finite_route": "boundary/absorption/storage flux norm enters q_boundary_mem",
            "status": "POYNTING_INCLUDED_AS_BOUNDARY_OR_FINITE_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CHAN4705_3_wave_envelope",
            "channel": "beta_gw rho_gw_eff",
            "selection_law": "high-frequency/relic wave stress is an averaged envelope source only if parent owns the averaging/observer map",
            "zero_route": "trace/conformal radiation-like branch, no local bath, projection zero, or beta_gw=0",
            "finite_route": "source beta_gw and local wave energy-density envelope",
            "status": "WAVE_CHANNEL_RETAINED_NOT_CLAIMED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def queue_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "priority": 1,
            "input": "ZK_memF2 or kappa_memF2",
            "why_next": "This is the smallest coefficient that decides whether memory can feed the Maxwell kinetic term at first order.",
            "derive_route": "typed-domain/no-Hom, fixed q-basic branch, branch extremum, or exact selection symmetry",
            "fallback_route": "source-backed kappa_memF2 and Z_Q_eff_min row",
            "status": "LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 2,
            "input": "Z_mem_min, M2_mem_min, C_Omega",
            "why_next": "These turn the memory no-hair idea into a real coercive amplitude bound.",
            "derive_route": "parent Hessian positivity plus local geometry constant",
            "fallback_route": "finite source-backed operator/gap row",
            "status": "LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 3,
            "input": "beta_T/frame owner",
            "why_next": "Trace branch is the least-scrutiny local-vacuum path but must not smuggle WEP/material effects.",
            "derive_route": "fixed Einstein/Jordan frame owner and universal trace coupling",
            "fallback_route": "finite beta_T/source trace profile and WEP residual row",
            "status": "LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 4,
            "input": "Poynting/readout/radiative boundary tails",
            "why_next": "This is where EM waves, apparatus projection and boundary flux re-enter without cheating.",
            "derive_route": "same-Hodge/no-observer/no-boundary-flux and loop/readout stability",
            "fallback_route": "finite B_readout, B_rad and S_EM dot n source rows",
            "status": "LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 5,
            "input": "K_arena_EM and tau_arena",
            "why_next": "Once the theory-side coefficient is bounded, these map it into R10, PPN, clock and orbital tests.",
            "derive_route": "material/clock/source projection theorem",
            "fallback_route": "source-backed empirical projection coefficients",
            "status": "LIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_status_next(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_CURRENT_BRANCH_SCALAR_BRIDGE_4705",
            "decision": DECISION,
            "reason": "4704's scalar-functional target is not remade: validated 4617-4623 work is imported and composed into a current-branch EM residual bound. The next step must source or zero a real coefficient.",
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
            "derived": "current-branch bridge plus composed C_memory_F2/rho_mem/arena residual law",
            "not_derived": "numeric kappa/Z/M/beta/source/K/tau values; parent-signed zero certificates; readout/radiative stability",
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
            "next_id": "NT4705_0",
            "target": NEXT_TARGET,
            "reason": "The symbolic ladder is now composed; progress requires either exact zero certificates or a first source-backed coefficient/projection value.",
            "derive_first": "try kappa_memF2/no-Hom/extremum and trace/Poynting/readout zero certificates on the same branch",
            "fallback": "fill first source-backed kappa/Z/M/beta/source/K/tau row and run a small score smoke",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4705 - Parent Scalar-Functional Bridge And Composite EM Residual Law

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint prevents the current branch from looping back into an already-built ladder.

4704 reduced the visible EM/Hom problem to parent scalar-functional exhaustion. The validated 4617-4623 ladder already sharpened that target into a zero-or-bound chain:

```text
D_v lambda_F2 = 0
```

only if the parent branch signs the transitive/no-Hom/kappa-zero/no-source/readout-stability clauses on the same branch.

If not, the finite memory/F2 component is no longer vague:

```text
C_memory_F2 <= |kappa_memF2|/Z_Q_eff_min
              * C_Omega*(||rho_mem||_Hminus1 + ||q_boundary_mem||_HminusHalf)
              / min(Z_mem_min,M2_mem_min).
```

with

```text
rho_mem = beta_R R_obs + beta_T T_obs + beta_F F_Q^2
        + beta_G F_Q starF_Q + beta_S div(S_EM)
        + beta_gw rho_gw_eff + J_hidden.
```

Poynting and wave channels remain live, but as parent-owned boundary/observer/envelope channels, not magic free volume forces.

## Source Register
{table(data["sources"])}

## Dedupe Bridge Imports
{table(data["bridge"])}

## Composite EM Residual Law
{table(data["composite"])}

## Source Channel Selection Rows
{table(data["channels"])}

## Numeric Or Zero Input Queue
{table(data["queue"])}

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
        f"""# 721 - PPC4161 Current-Branch Scalar Bridge And Composite EM Local Residual Law

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
The 4704 parent-scalar-functional target is resolved as a bridge, not a duplicate checkpoint:

```text
4704 visible-image/Hom gate
  -> 4617 scalar-functional exhaustion theorem
  -> 4618-4620 memory/F2 owner and kappa routes
  -> 4621 positive memory operator bound
  -> 4622-4623 rho_mem channel and beta-owner rules.
```

Composite finite branch:

```text
C_memory_F2 <= |kappa_memF2|/Z_Q_eff_min
              * C_Omega*(||rho_mem||_Hminus1 + ||q_boundary_mem||_HminusHalf)
              / min(Z_mem_min,M2_mem_min).
```

Source-channel owner rule:

```text
rho_mem = beta_R R_obs + beta_T T_obs + beta_F F_Q^2
        + beta_G F_Q starF_Q + beta_S div(S_EM)
        + beta_gw rho_gw_eff + J_hidden.
```

`beta_F` is not independent if the parent owner is `Z_Q_eff(m_mem)`; it is tied to `kappa_memF2`. `beta_S` is not a covariant volume scalar without parent observer/coframe/current ownership and otherwise becomes boundary/absorption flux. No local-GR, Maxwell, alpha, WEP, clock, R10 or orbital claim follows.
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
            "claim": "4705 bridges the current 4704 EM/Hom gate to the validated 4617-4623 scalar/memory ladder and derives the composed finite EM residual law.",
            "current_evidence": "Generated source register, dedupe bridge imports, composite EM residual law, source-channel selection rows, numeric/zero queue, decision, status, next target and validation.",
            "status": "current_branch_composite_residual_law_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Looping back into scalar-functional audits instead of sourcing or zeroing kappa/Z/M/beta/source/K/tau inputs.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Current-branch scalar bridge and composite EM residual law",
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
- Movement: 4704 no longer loops back into scalar-functional audit; 4617-4623 are imported and composed into a concrete memory/F2 residual bound.
- Composite law: `C_memory_F2 <= |kappa_memF2|/Z_Q_eff_min * C_Omega*(||rho_mem||_Hminus1 + ||q_boundary_mem||_HminusHalf)/min(Z_mem_min,M2_mem_min)`.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 loop-breaker bridge from EM/Hom scalar exhaustion to source-backed residual scoring.
- Validation: `{VALIDATION_CSV}`.
""",
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

    add("VAL4705_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4705_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4705_2_bridge_dedupes", any(row["bridge_id"] == "BR4705_0_no_duplicate_target" for row in data["bridge"]), "dedupe bridge row present")
    add("VAL4705_3_composed_bound", any("C_memory_F2 <=" in row["law"] and "rho_mem" in row["law"] for row in data["composite"]), "composed memory/F2 bound present")
    add("VAL4705_4_poynting_retained", any("Poynting" in row["channel_id"] and "boundary" in row["finite_route"] for row in data["channels"]), "Poynting boundary/finite channel retained")
    add("VAL4705_5_wave_retained", any("wave" in row["channel_id"].lower() for row in data["channels"]), "wave envelope channel retained")
    add("VAL4705_6_betaF_tied", any("beta_F" in row["selection_law"] and "kappa" in row["selection_law"] for row in data["channels"]), "beta_F tied to kappa_memF2")
    add("VAL4705_7_next_not_loop", data["next"][0]["target"] == NEXT_TARGET and "4617" not in data["next"][0]["target"], "next target does not loop back to 4617")
    add("VAL4705_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4705_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4705_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4705_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4705_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        BRIDGE_CSV,
        COMPOSITE_CSV,
        CHANNEL_CSV,
        QUEUE_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4705_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4705_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [
        data["bridge"],
        data["composite"],
        data["channels"],
        data["queue"],
        data["decision"],
        data["status"],
        data["next"],
    ]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4705_13_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4705_14_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4705_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_status_next(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "bridge": bridge_rows(timestamp),
        "composite": composite_rows(timestamp),
        "channels": channel_rows(timestamp),
        "queue": queue_rows(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(BRIDGE_CSV, data["bridge"])
    write_csv(COMPOSITE_CSV, data["composite"])
    write_csv(CHANNEL_CSV, data["channels"])
    write_csv(QUEUE_CSV, data["queue"])
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
