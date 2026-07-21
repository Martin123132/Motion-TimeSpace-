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

CHECKPOINT = "4683"
CLAIM_ID = "L-525"
MARKER = "PPC4161_MEMORY_FIBRE_BC_OWNER_BODY_CHARGE_CURRENT_BRANCH_4683"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_FIBRE_BC_OWNER_BODY_CHARGE_CURRENT_BRANCH_4683"
DECISION = "MEMORY_FIBRE_ZERO_SWITCH_AND_BODY_CHARGE_BOUND_IMPORTED_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4684-Y5-R2FR-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md"

DOC_PATH = POST / "4683-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"
FORMAL_PATH = FORMAL / "699-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4682_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4682_NEXT_TARGET.csv"
CSV_4682_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4682_STATUS.csv"
CSV_4595_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4595_OWNER_ZERO_SWITCH.csv"
CSV_4595_MEM_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4595_MEMORY_BODY_CHARGE_BOUND.csv"
CSV_4595_FIB_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4595_FIBRE_BODY_CHARGE_BOUND.csv"
CSV_4595_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4595_BMEM_EFF_INSERTION.csv"
CSV_4595_SCHEMA = SOURCE_DIR / "P8_Y5_R2FR_4595_FINITE_INPUT_SCHEMA.csv"
CSV_4595_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4595_STATUS.csv"
CSV_4595_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4595_NEXT_TARGET.csv"
CSV_4595_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4595_VALIDATION.csv"
CSV_4596_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4596_STATUS.csv"
CSV_4596_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4596_NEXT_TARGET.csv"
CSV_4596_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4596_VALIDATION.csv"
FORMAL_611 = FORMAL / "611-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4683_SOURCE_REGISTER.csv"
ZERO_SWITCH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_OWNER_ZERO_SWITCH.csv"
MEMORY_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_MEMORY_BODY_CHARGE_BOUND.csv"
FIBRE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_FIBRE_BODY_CHARGE_BOUND.csv"
BMEM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_BMEM_EFF_INSERTION.csv"
FINITE_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_FINITE_INPUT_SCHEMA.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4683_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4683_VALIDATION.csv"


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
        ("SRC4683_00_4682_next", CSV_4682_NEXT, "4683-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md", "4682 selected memory/fibre owner target."),
        ("SRC4683_01_4682_status", CSV_4682_STATUS, "memory/fibre B,C,J,Q_boundary zero switch", "4682 status identifies next owner target."),
        ("SRC4683_02_4595_owner", CSV_4595_OWNER, "ZS4595_0_common_operator", "common memory/fibre zero switch."),
        ("SRC4683_03_4595_memory_bound", CSV_4595_MEM_BOUND, "MEM4595_2_amplitude", "memory body-charge amplitude bound."),
        ("SRC4683_04_4595_fibre_bound", CSV_4595_FIB_BOUND, "FIB4595_2_amplitude", "fibre body-charge amplitude bound."),
        ("SRC4683_05_4595_bmem", CSV_4595_BMEM, "BM4595_5_combined", "B_mem_eff absolute-sum insertion."),
        ("SRC4683_06_4595_schema", CSV_4595_SCHEMA, "schema4595_12_projection", "finite input schema."),
        ("SRC4683_07_4595_status", CSV_4595_STATUS, "MEMORY_FIBRE_BC_ZERO_SWITCH", "4595 status."),
        ("SRC4683_08_4595_next", CSV_4595_NEXT, "memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row", "4595 next target."),
        ("SRC4683_09_4595_validation", CSV_4595_VALIDATION, "VAL4595_OVERALL", "4595 validation passed."),
        ("SRC4683_10_4596_status", CSV_4596_STATUS, "STRICT_SOURCE_KERNEL_INSERTED", "4596 source-kernel insertion already exists."),
        ("SRC4683_11_4596_next", CSV_4596_NEXT, "4597-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md", "4596 next target."),
        ("SRC4683_12_4596_validation", CSV_4596_VALIDATION, "VAL4596_OVERALL", "4596 validation passed."),
        ("SRC4683_13_formal611", FORMAL_611, "B_X=C_X=J_X=Q_boundary_X=0", "formal memory/fibre zero switch."),
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


def zero_switch_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ZS4683_0_common_operator", "X in {memory m, finite-cell fibre h}", "L_X delta_X = (-Z_X nabla^2 + M_X^2) delta_X = rho_X", "rho_X = B_X R_obs + C_X T + J_X", "Z_X>0; M_X^2>0; zero modes removed; B_X=C_X=J_X=Q_boundary_X=0 in the same parent branch => delta_X=0 and A_X=0", "|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary_X|]/(4*pi |Z_X|)", "DERIVED_COMMON_ZERO_OR_BOUND_LAW"),
        ("ZS4683_1_memory", "memory/class scalar m", "L_mem delta_m = rho_mem; lambda_mem=sqrt(Z_mem/M2_mem)", "rho_mem = B_mem_eff R_obs + C_mem T + J_mem", "B_mem_eff=C_mem=J_mem=Q_boundary_mem=0 plus positive L_mem and zero-mode removal => A_mem=0", "absolute B_mem_eff/C_mem/J_mem/Q_boundary_mem source envelope; no cancellation credit", "MEMORY_ZERO_SWITCH_DERIVED_CONDITIONAL_UNSIGNED"),
        ("ZS4683_2_fibre", "finite-cell fibre h", "L_h delta_h = rho_h; lambda_h=sqrt(Z_h/M2_h)", "rho_h = B_h R_obs + C_h T + J_h", "B_h=C_h=J_h=Q_boundary_h=0 plus positive L_h and zero-mode removal => A_h=0", "source Z_h,M2_h,B_h,C_h,J_h,Q_boundary_h and body profile; then compare induced alpha(lambda_h)", "FIBRE_ZERO_SWITCH_DERIVED_CONDITIONAL_UNSIGNED"),
        ("ZS4683_3_no_smuggling", "positive hidden/memory/fibre operator", "0.5 B^T L^-1 B = 0.5 ||L^-1/2 B||^2", "nonzero B_X or nonzero C_X/J_X/boundary creates a body charge even with positive L_X", "positive L_X is useful only after source silence is signed", "0.5 ||B_X||^2/lambda_min(L_X) plus body-charge bound", "COUNTERMODEL_GUARD_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "switch_id": switch_id,
            "object": obj,
            "equation": equation,
            "rho_definition": rho,
            "zero_switch": zero,
            "finite_exit": finite_exit,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for switch_id, obj, equation, rho, zero, finite_exit, status in data
    ]


def memory_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("MEM4683_0_density", "memory source density", "rho_mem = B_mem_eff R_obs + C_mem T + J_mem", "B_mem_eff=C_mem=J_mem=0", "||rho_mem|| <= ||B_mem_eff|| ||R_obs|| + ||C_mem|| ||T|| + ||J_mem||", "B_mem_eff;C_mem;J_mem;R_obs;T;source units;source paths"),
        ("MEM4683_1_body_charge", "memory body charge", "Q_mem0=4*pi int_0^R dr r^2 rho_mem(r) sinh(r/lambda_mem)/(r/lambda_mem)+Q_boundary_mem", "rho_mem=0 and Q_boundary_mem=0, or exact weighted cancellation explicitly parent-owned", "|Q_mem0| <= exp(R_body/lambda_mem) int_body ||rho_mem|| dV + ||Q_boundary_mem||", "lambda_mem;R_body;rho_mem profile;Q_boundary_mem"),
        ("MEM4683_2_amplitude", "exterior memory amplitude", "|A_mem| <= [exp(R_body/lambda_mem) int_body (||B_mem_eff||||R_obs||+||C_mem||||T||+||J_mem||) dV + ||Q_boundary_mem||]/(4*pi ||Z_mem||)", "positive L_mem plus B_mem_eff=C_mem=J_mem=Q_boundary_mem=0", "if nonzero, map A_mem/lambda_mem to alpha_mem(lambda_mem), R10/orbital/PPN residual", "Z_mem;M2_mem;lambda_mem;B_mem_eff;C_mem;J_mem;Q_boundary_mem;arena projection"),
        ("MEM4683_3_poynting_guard", "J_mem EM/Poynting subchannel", "J_mem = J_nonHilbert + J_EM_flux; J_EM_flux=0 only under same_Hodge + same_current_owner + stationary_tau + no_radiative_boundary_flux", "EM stress is inside common Hilbert T_tot and no Poynting flux crosses the local worldtube boundary", "||J_EM_flux|| <= ||Phi_EM_rad||+||W_public_exchange||+||C_EM_surface_gauge||", "same-Hodge/current owner certificate; Poynting flux collar; boundary/source paths"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "target": target,
            "formula": formula,
            "zero_condition": zero,
            "bound": bound,
            "needed_inputs": needed,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, target, formula, zero, bound, needed in data
    ]


def fibre_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("FIB4683_0_density", "finite-cell fibre source density", "rho_h = B_h R_obs + C_h T + J_h", "B_h=C_h=J_h=0", "||rho_h|| <= ||B_h||||R_obs|| + ||C_h||||T|| + ||J_h||", "B_h;C_h;J_h;R_obs;T;source units;source paths"),
        ("FIB4683_1_body_charge", "finite-cell fibre body charge", "Q_h0=4*pi int_0^R dr r^2 rho_h(r) sinh(r/lambda_h)/(r/lambda_h)+Q_boundary_h", "rho_h=0 and Q_boundary_h=0, or exact weighted cancellation explicitly parent-owned", "|Q_h0| <= exp(R_body/lambda_h) int_body ||rho_h|| dV + ||Q_boundary_h||", "lambda_h;R_body;rho_h profile;Q_boundary_h"),
        ("FIB4683_2_amplitude", "exterior fibre amplitude", "|A_h| <= [exp(R_body/lambda_h) int_body (||B_h||||R_obs||+||C_h||||T||+||J_h||) dV + ||Q_boundary_h||]/(4*pi ||Z_h||)", "positive L_h plus B_h=C_h=J_h=Q_boundary_h=0", "if nonzero, map A_h/lambda_h to alpha_h(lambda_h), R10/orbital/PPN residual", "Z_h;M2_h;lambda_h;B_h;C_h;J_h;Q_boundary_h;arena projection"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "target": target,
            "formula": formula,
            "zero_condition": zero,
            "bound": bound,
            "needed_inputs": needed,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, target, formula, zero, bound, needed in data
    ]


def bmem_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BM4683_0_B826", "B_826", "earlier parent trace/branch extremum coefficient is theorem-zero in the same memory branch", "|B_826| retained as absolute coefficient if not zero", "IMPORTED_COMPONENT_UNSIGNED"),
        ("BM4683_1_BWeyl", "B_Weyl_vec", "source-root/no-spurion/Khat gate zeros the Weyl-response tail", "||B_Weyl_vec|| retained from component vector", "IMPORTED_COMPONENT_UNSIGNED"),
        ("BM4683_2_Y5", "B_Y5_trace", "single q-basic Hilbert mass-current/source functor with universal calibration", "||B_Y5_trace|| <= sum_i ||j_Z,Y5_i|| ||P_i||", "PARTIAL_STATIONARY_CLOSURE_ONLY"),
        ("BM4683_3_Y6", "B_Y6_trace", "extra stress is topological/invisible, EH-owned metric response, or exchange-even", "||B_Y6_trace|| <= sum_j ||j_Z,Y6_j|| ||X_j||", "VECTOR_IMPORTED_UNSIGNED"),
        ("BM4683_4_boundary_readout", "B_src_boundary + B_src_readout", "no source boundary/readout leakage through local worldtube and same observed frame", "absolute boundary/readout coefficients remain in Sigma_B", "TAIL_IMPORTED_UNSIGNED"),
        ("BM4683_5_combined", "B_mem_eff", "B_826=B_Weyl_vec=B_Y5_trace=B_Y6_trace=B_src_boundary=B_src_readout=0 in same parent branch", "||B_mem_eff|| <= ||B_826||+||B_Weyl_vec||+||B_Y5_trace||+||B_Y6_trace||+||B_src_boundary||+||B_src_readout||", "ABSOLUTE_SUM_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "component": component,
            "zero_condition": zero,
            "finite_bound": finite_bound,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, component, zero, finite_bound, status in data
    ]


def schema_rows(timestamp: str) -> list[dict[str, Any]]:
    symbols = [
        ("memory", "Z_mem", "operator normalization"),
        ("memory", "M2_mem", "operator mass gap"),
        ("memory", "B_mem_eff components", "curvature-linear source vector"),
        ("memory", "C_mem", "matter-trace coupling"),
        ("memory", "J_mem", "direct/non-Hilbert/Poynting current"),
        ("memory", "Q_boundary_mem", "worldtube/boundary charge"),
        ("fibre", "Z_h", "operator normalization"),
        ("fibre", "M2_h", "operator mass gap"),
        ("fibre", "B_h", "curvature-linear fibre vertex"),
        ("fibre", "C_h", "matter-trace fibre coupling"),
        ("fibre", "J_h", "direct fibre current"),
        ("fibre", "Q_boundary_h", "fibre boundary charge"),
        ("arena", "Pi_R10/Pi_PPN/Pi_orbital", "observable projection"),
    ]
    rows = []
    for index, (sector, symbol, role) in enumerate(symbols):
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "input_id": f"schema4683_{index}",
                "sector": sector,
                "symbol": symbol,
                "role": role,
                "required_for_claim": "parent-signed zero or numeric/source-backed value",
                "current_status": "MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4683_0_memory_fibre_zero_switch", "memory/fibre B,C,J,boundary owner", "zero-switch law imported; parent signatures/numeric values still missing", NEXT_TARGET),
        ("SURV4683_1_cR2_MR", "c_R2/M_R finite-range curvature branch", "reduced to memory/fibre owner/source rows or finite body-charge bound", NEXT_TARGET),
        ("SURV4683_2_cGamma", "c_Gamma local memory coupling", "unchanged broad survivor", "derive support/projector zero or source coefficients after current memory/fibre source work"),
        ("SURV4683_3_EH_principal", "EH principal / public parent adoption", "still public blocker", "retain parent selector/adoption gate"),
        ("SURV4683_4_material_projection_global", "Lambda/material/projection/global parent", "unchanged blocker", "keep promotion firewall active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4683": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4683_0", "Positive L_X does not close memory/fibre if B_X, C_X, J_X or Q_boundary_X is nonzero."),
        ("CTRL4683_1", "Exterior source-free equations do not erase A_mem/A_h body charge."),
        ("CTRL4683_2", "B_mem_eff must be an absolute-sum ledger; no cancellation between B826/Weyl/Y5/Y6/boundary/readout pieces."),
        ("CTRL4683_3", "Poynting/EM flux is retained inside J_mem unless same-Hodge/current/no-flux guards are signed."),
        ("CTRL4683_4", "Next move is source-functor descent or first finite J_live/body-charge norm, not another cR2 label pass."),
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
            "summary": "4683 imports the validated 4595 memory/fibre zero-switch gate into the current branch. For X in {memory, fibre}, local silence needs positive operator, zero modes removed, and B_X=C_X=J_X=Q_boundary_X=0 in the same parent branch. If unsigned, the branch is finite and scored by A_mem/A_h body-charge bounds. B_mem_eff is an absolute-sum ledger and Poynting remains inside J_mem unless its same-Hodge/current/no-flux guards are signed.",
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
            "derived": "common memory/fibre zero switch; B_mem_eff absolute-sum insertion; A_mem and A_h body-charge bounds; finite-input schema; Poynting guard",
            "not_derived": "parent-signed B_mem_eff=C_mem=J_mem=Q_boundary_mem=0; parent-signed B_h=C_h=J_h=Q_boundary_h=0; numeric Z/M2/source coefficients; arena projections",
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
            "next_id": "NT4683_0",
            "target": NEXT_TARGET,
            "reason": "4683 reduces memory/fibre cR2 pressure rows to a concrete zero switch or finite body-charge coefficient schema.",
            "derive_first": "parent-sign source functor descent for C_mem/C_h and J_live silence, including EM/Hodge/support/readout q-basic/h-blind clauses",
            "fallback": "fill first finite norm row for J_X^EM_open, J_X^nonHilbert, J_X^dyn_exchange or Q_boundary_X",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4683 - Y5/R2FR Memory/Fibre B_X C_X Owner Or Body-Charge Input After cR2 Gate

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4683 imports the current memory/fibre zero-switch gate:

```text
L_X delta_X = (-Z_X nabla^2 + M_X^2) delta_X = rho_X
rho_X = B_X R_obs + C_X T + J_X
Z_X>0, M_X^2>0, zero modes removed,
B_X=C_X=J_X=Q_boundary_X=0
=> delta_X=0 and A_X=0.
```

If any source term is unsigned, the branch is finite:

```text
|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV
          + |Q_boundary_X|] / (4*pi |Z_X|).
```

For memory, `B_X = B_mem_eff` and is carried as an absolute-sum ledger. For fibre, `B_X = B_h`. EM/Poynting is not hidden; it remains in `J_mem` unless same-Hodge/current/no-flux guards are signed.

## Source Register

{table(rows["sources"])}

## Owner Zero Switch

{table(rows["zero_switch"])}

## Memory Body-Charge Bound

{table(rows["memory_bounds"])}

## Fibre Body-Charge Bound

{table(rows["fibre_bounds"])}

## B_mem_eff Insertion

{table(rows["bmem"])}

## Finite Input Schema

{table(rows["schema"])}

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
    FORMAL_PATH.write_text(body.replace("# 4683 - Y5/R2FR", "# 699 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4683 imports the memory/fibre zero-switch gate into the current branch: for X in {memory,fibre}, local silence requires positive operator, zero modes removed, and B_X=C_X=J_X=Q_boundary_X=0 in the same parent branch; otherwise A_mem/A_h body-charge bounds remain finite. B_mem_eff is an absolute-sum ledger and Poynting remains guarded inside J_mem.",
                "current_evidence": "Generated source register, owner zero switch, memory and fibre body-charge bounds, Bmem effective insertion, finite input schema, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Using positive operator, exterior source-free equations, fitted G, or EM/Poynting flow to erase nonzero B,C,J,boundary source charges.",
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
        f"""## Local GR Parent-Derivation Update - Current Memory/Fibre Zero Switch

Marker: `{MARKER}`

4683 imports the memory/fibre zero switch into the current branch:

```text
L_X delta_X = rho_X,
rho_X = B_X R_obs + C_X T + J_X,
B_X=C_X=J_X=Q_boundary_X=0 => A_X=0.
```

If the zero switch is unsigned, `A_mem` and `A_h` are finite body-charge envelopes. `B_mem_eff` is an absolute-sum ledger and Poynting remains inside `J_mem` unless guarded out. The next target is source-functor descent or first finite `J_live`/body-charge norm.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Memory/Fibre Zero Switch

Marker: `{PACKET_MARKER}`

The packet now has a concrete memory/fibre owner gate: source-functor descent or first finite body-charge coefficient row. Do not hide EM/Poynting, fitted G, or source calibration outside `J_mem/J_h`.

- zero-switch csv: `{ZERO_SWITCH_CSV.name}`
- finite schema csv: `{FINITE_SCHEMA_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4683_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4683_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4683_2_zero_switch", any(row["switch_id"] == "ZS4683_0_common_operator" for row in rows["zero_switch"]), "common zero switch present"),
        ("VAL4683_3_memory_bound", any(row["bound_id"] == "MEM4683_2_amplitude" for row in rows["memory_bounds"]), "memory amplitude bound present"),
        ("VAL4683_4_fibre_bound", any(row["bound_id"] == "FIB4683_2_amplitude" for row in rows["fibre_bounds"]), "fibre amplitude bound present"),
        ("VAL4683_5_bmem_absolute_sum", any(row["component"] == "B_mem_eff" for row in rows["bmem"]), "B_mem_eff absolute-sum row present"),
        ("VAL4683_6_schema", len(rows["schema"]) == 13, "finite input schema has 13 rows"),
        ("VAL4683_7_next_source_functor", rows["next"][0]["target"] == NEXT_TARGET, "next source-functor target selected"),
        ("VAL4683_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-525"),
        ("VAL4683_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4683_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4683_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4683_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4683_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4683_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4683_13_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4683_14_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4683_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "zero_switch": zero_switch_rows(timestamp),
        "memory_bounds": memory_bound_rows(timestamp),
        "fibre_bounds": fibre_bound_rows(timestamp),
        "bmem": bmem_rows(timestamp),
        "schema": schema_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        ZERO_SWITCH_CSV: rows["zero_switch"],
        MEMORY_BOUND_CSV: rows["memory_bounds"],
        FIBRE_BOUND_CSV: rows["fibre_bounds"],
        BMEM_CSV: rows["bmem"],
        FINITE_SCHEMA_CSV: rows["schema"],
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
