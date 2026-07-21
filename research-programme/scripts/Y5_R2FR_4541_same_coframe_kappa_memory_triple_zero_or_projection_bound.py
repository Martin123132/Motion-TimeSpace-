from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4541"
CLAIM_ID = "L-383"
BRANCH_ID = "MTS_R2FR_Y5_SAME_COFRAME_KAPPA_MEMORY_TRIPLE_ZERO_OR_BOUND_4541"
MARKER = "PPC4161_SAME_COFRAME_KAPPA_MEMORY_TRIPLE_ZERO_UNDER_EFFECTIVE_LOCAL_BRANCH_OR_PROJECTION_BOUND_4541"
PACKET_MARKER = "PPC4161_PACKET_SAME_COFRAME_KAPPA_MEMORY_TRIPLE_ZERO_UNDER_EFFECTIVE_LOCAL_BRANCH_OR_PROJECTION_BOUND_4541"
DECISION = "CD_AND_DELTAKAPPA_PRIVATE_ZERO_IMPORTED_CGAMMA_PARENT_ZERO_REJECTED_CGAMMA_PROJECTION_BOUND_ROUTE_ACTIVE"
NEXT_TARGET = "4542-Y5-R2FR-cGamma-parent-memory-equation-or-first-projection-bound-row.md"

FORMAL_PATH = FORMAL / "557-PPC4161-same-coframe-kappa-memory-triple-zero-under-effective-local-branch-or-projection-bound.md"
DOC_PATH = POST / "4541-Y5-R2FR-same-coframe-kappa-memory-triple-zero-under-effective-local-branch-or-projection-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4541_SOURCE_REGISTER.csv"
TRIPLE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4541_TRIPLE_ZERO_AUDIT.csv"
ZERO_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4541_PRIVATE_ZERO_LAWS.csv"
CGAMMA_OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4541_CGAMMA_OBSTRUCTION_LEDGER.csv"
PROJECTION_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4541_CGAMMA_PROJECTION_BOUND_ROUTE.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4541_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4541_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4541_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4541_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4541_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
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
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4541_00_4540_status",
            "label": "4540 priority triple",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4540_STATUS.csv",
            "needle": "priority_coefficients",
            "role": "4540 identifies c_D, delta_kappa, c_Gamma as priority coefficients",
        },
        {
            "source_id": "SRC4541_01_4540_envelope",
            "label": "4540 EFT envelope",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4540_EFT_RESIDUAL_ENVELOPE.csv",
            "needle": "EFT4540_3_cGamma",
            "role": "active residual envelope for the priority triple",
        },
        {
            "source_id": "SRC4541_02_4186_status",
            "label": "4186 joint zero status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4186_STATUS.csv",
            "needle": "c_D_private_zero",
            "role": "same-coframe/source roots already zero privately",
        },
        {
            "source_id": "SRC4541_03_4186_firewall",
            "label": "4186 claim firewall",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4186_CLAIM_FIREWALL.csv",
            "needle": "c_Gamma needs its own local memory support/projector theorem",
            "role": "prevents c_Gamma from piggybacking on c_D/delta_kappa",
        },
        {
            "source_id": "SRC4541_04_4187_status",
            "label": "4187 cGamma status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4187_STATUS.csv",
            "needle": "c_Gamma_parent_zero",
            "role": "c_Gamma parent zero remains false",
        },
        {
            "source_id": "SRC4541_05_4187_routes",
            "label": "4187 cGamma zero route audit",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4187_CGAMMA_ZERO_ROUTE_AUDIT.csv",
            "needle": "ZR4187_5_homogeneous_tensor",
            "role": "hard obstruction from homogeneous tensor residue",
        },
        {
            "source_id": "SRC4541_06_4187_contract",
            "label": "4187 support projector contract",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4187_MEMORY_SUPPORT_PROJECTOR_CONTRACT.csv",
            "needle": "SP4187_8_claim_gate",
            "role": "all memory clauses needed for c_Gamma zero",
        },
        {
            "source_id": "SRC4541_07_4187_bounds",
            "label": "4187 finite cGamma bound interface",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4187_FINITE_CGAMMA_BOUND_INTERFACE.csv",
            "needle": "FB4187_2_orbital",
            "role": "finite bound interface for c_Gamma",
        },
        {
            "source_id": "SRC4541_08_4188_status",
            "label": "4188 finite product bounds",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4188_STATUS.csv",
            "needle": "product_bounds_available",
            "role": "finite c_Gamma product bound law exists nonclaim",
        },
        {
            "source_id": "SRC4541_09_4189_status",
            "label": "4189 projection split",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4189_STATUS.csv",
            "needle": "CGamma_Gdot_formula_filled",
            "role": "symbolic metric/Gdot projection split exists",
        },
        {
            "source_id": "SRC4541_10_4190_status",
            "label": "4190 stationarity profile",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4190_STATUS.csv",
            "needle": "finite_profile_bounds_ready",
            "role": "stationarity alone does not close zero but profile bounds are ready",
        },
        {
            "source_id": "SRC4541_11_4196_status",
            "label": "4196 scalar leakage pruning",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4196_STATUS.csv",
            "needle": "STATIONARITY_ALONE_REJECTED",
            "role": "later scalar route rejects stationarity-only zero",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def triple_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient": "c_D",
            "meaning": "same-coframe/disformal second-metric owner leakage",
            "best_zero_route": "all matter, clocks and Maxwell-Hodge actions descend through one q-owned observed coframe g_obs",
            "current_4541_status": "PRIVATE_ZERO_IMPORTED_FROM_4186",
            "global_parent_status": "not_global_claim",
            "fallback_if_reopened": "WEP/clock/EM propagation projection bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "coefficient": "delta_kappa",
            "meaning": "source-coupling/kappa drift or source-measure multiplier",
            "best_zero_route": "topological kappa lock plus Hilbert source-measure descent with no species/readout multiplier",
            "current_4541_status": "PRIVATE_ZERO_IMPORTED_FROM_4186",
            "global_parent_status": "numeric_G_calibrated_not_predicted",
            "fallback_if_reopened": "LLR Gdot/G, measured-G envelope, orbital GM consistency",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "coefficient": "c_Gamma",
            "meaning": "MTS-specific local memory coupling/hair",
            "best_zero_route": "Gamma_mem vertical/support/boundary/no-hair/tensor clauses all parent-owned",
            "current_4541_status": "PARENT_ZERO_REJECTED_BOUND_ROUTE_ACTIVE",
            "global_parent_status": "open_core_MTS_local_risk",
            "fallback_if_reopened": "PPN/clock/orbital/R10 projection-bound rows with no-cancellation guards",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def zero_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "zero_law_id": "ZL4541_0_same_coframe",
            "target": "c_D",
            "law": "If the parent local branch has exactly one observed coframe/metric functor and matter, clocks and Maxwell-Hodge all factor through it before readout, then no disformal/second-metric coefficient exists in the active local source action.",
            "formula": "S_matter,S_EM,S_clock -> S[fields,g_obs]; no Hom(readout_label, metric_owner) => c_D=0",
            "status": "PRIVATE_ZERO_UNDER_EFFECTIVE_BRANCH",
            "scope": "PPC4161-GP-HQNP effective local branch only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_law_id": "ZL4541_1_kappa_source_lock",
            "target": "delta_kappa",
            "law": "If kappa_* is topological/superselected and the Hilbert source measure descends with no source/readout multiplier, then no local kappa/source drift coefficient survives.",
            "formula": "D_A ln kappa_*=0 and delta Z_H=0 => delta_kappa=0",
            "status": "PRIVATE_ZERO_UNDER_EFFECTIVE_BRANCH",
            "scope": "structural coupling only; numeric G remains calibrated",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_law_id": "ZL4541_2_memory_not_inherited",
            "target": "c_Gamma",
            "law": "c_Gamma does not vanish merely because c_D and delta_kappa vanish; it needs its own memory support/projector/no-hair theorem.",
            "formula": "c_D=0 and delta_kappa=0 does not imply P_loc(delta S_Gamma/delta O_loc)=0",
            "status": "ZERO_REJECTED_CURRENT_CORPUS",
            "scope": "all local public claims blocked until c_Gamma zero or bound rows exist",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def cgamma_obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "CGO4541_0_horizontal",
            "route": "vertical quotient",
            "obstruction": "Gamma_mem may have a q-horizontal component, so representative vertical silence is not enough.",
            "required_to_close": "prove Gamma_mem in ker(Dq) or split and bound Gamma_horizontal",
            "status": "OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "obstruction_id": "CGO4541_1_support",
            "route": "compact support",
            "obstruction": "no parent theorem shows P_loc Gamma_mem=0 in compact local collars; constant memory can renormalize coefficients.",
            "required_to_close": "derive support separation or screening scale from parent memory equation",
            "status": "OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "obstruction_id": "CGO4541_2_boundary",
            "route": "boundary routing",
            "obstruction": "known no-flux routing does not identify c_Gamma-specific memory flux as pure boundary charge.",
            "required_to_close": "derive J_Gamma_bulk=0 and F_Gamma_boundary as the only memory term",
            "status": "OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "obstruction_id": "CGO4541_3_nohair",
            "route": "positive/no-hair",
            "obstruction": "operator, sign, source term and boundary data are not all parent-owned.",
            "required_to_close": "construct positive L_Gamma, prove J_Gamma=0, lock boundary data",
            "status": "OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "obstruction_id": "CGO4541_4_tensor",
            "route": "homogeneous tensor residue",
            "obstruction": "scalar support silence does not kill divergence-free Gamma_perp/K_perp tensor modes.",
            "required_to_close": "prove tensor boundary no-hair or include Gamma_perp in finite residual vector",
            "status": "HARD_OBSTRUCTION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def projection_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "PB4541_0_master",
            "arena": "all local arenas",
            "bound_law": "|R_A^Gamma| <= |J_A^Gamma| |c_Gamma| ||P_A Gamma_mem|| + |J_A^perp| ||Gamma_perp/K_perp||",
            "inputs_needed": "c_Gamma, arena projection J_A^Gamma, memory profile norm, tensor/perp norm, source-backed threshold",
            "status": "BOUND_ROUTE_ACTIVE_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PB4541_1_PPN",
            "arena": "PPN",
            "bound_law": "compare ||R_PPN^Gamma|| to PPN residual thresholds",
            "inputs_needed": "J_PPN^Gamma, Gamma profile, Gamma_perp/K_perp, PPN threshold table",
            "status": "projection_missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PB4541_2_clock",
            "arena": "clock/redshift",
            "bound_law": "compare fractional clock/redshift memory projection to source-backed clock bounds",
            "inputs_needed": "J_clock^Gamma, local environmental profile, units, threshold source",
            "status": "projection_missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PB4541_3_orbital",
            "arena": "orbital/LLR/Gdot",
            "bound_law": "compare memory-induced acceleration, perihelion or Gdot term to orbital envelope",
            "inputs_needed": "J_orbital^Gamma, radial profile, Gdot/perihelion threshold",
            "status": "best_first_empirical_fallback",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PB4541_4_R10",
            "arena": "R10 short-range",
            "bound_law": "compare alpha_Gamma(lambda) to real alpha_bound(lambda)",
            "inputs_needed": "lambda_Gamma, alpha_Gamma(lambda), reviewed/digitized bound curve",
            "status": "deferred_until_projection_and_curve",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4541_0_cD",
            "gate": "same-coframe c_D",
            "status": "PASS_PRIVATE_ZERO",
            "meaning": "c_D=0 inside the effective local branch, not global parent theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4541_1_deltaKappa",
            "gate": "kappa/source delta_kappa",
            "status": "PASS_PRIVATE_ZERO",
            "meaning": "delta_kappa=0 structurally inside the branch; numeric G not predicted",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4541_2_cGamma",
            "gate": "memory c_Gamma parent zero",
            "status": "FAIL_PARENT_ZERO_OPEN",
            "meaning": "c_Gamma remains the active local memory coefficient",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4541_3_bound_route",
            "gate": "finite c_Gamma projection-bound route",
            "status": "ACTIVE_NONCLAIM",
            "meaning": "bound route exists but needs projection coefficients and source-backed thresholds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4541_4_public_local_GR",
            "gate": "public local-GR claim",
            "status": "BLOCKED_NONCLAIM",
            "meaning": "public claim remains blocked while c_Gamma has no parent zero or finite validated bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4541_0",
            "decision": DECISION,
            "meaning": "4541 imports the strongest older triple-zero result into the current 4540 chain: c_D and delta_kappa are private zeros in the effective local branch, but c_Gamma is not inherited and stays as the primary memory residual with an explicit projection-bound route.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4541_0",
            "target": NEXT_TARGET,
            "objective": "try to derive a parent memory equation for c_Gamma or fill the first real projection-bound row",
            "derive_first": "parent memory equation with support/no-hair/tensor clauses",
            "fallback": "first projection-bound row, preferably orbital/Gdot or PPN before R10",
            "avoid": "claiming R10 or local-GR pass from c_D/delta_kappa zeros alone",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "c_D_private_zero": "True",
            "delta_kappa_private_zero": "True",
            "c_Gamma_parent_zero": "False",
            "c_Gamma_projection_bound_route_active": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    triple: list[dict[str, Any]],
    zero_laws: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4541_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    private_zero_ok = any(row["coefficient"] == "c_D" and row["current_4541_status"] == "PRIVATE_ZERO_IMPORTED_FROM_4186" for row in triple) and any(row["coefficient"] == "delta_kappa" and row["current_4541_status"] == "PRIVATE_ZERO_IMPORTED_FROM_4186" for row in triple)
    checks.append({"validation_id": "VAL4541_01_private_zeros", "status": "PASS" if private_zero_ok else "FAIL", "detail": "c_D and delta_kappa private zeros imported"})

    cgamma_open_ok = any(row["coefficient"] == "c_Gamma" and row["current_4541_status"] == "PARENT_ZERO_REJECTED_BOUND_ROUTE_ACTIVE" for row in triple)
    checks.append({"validation_id": "VAL4541_02_cGamma_open", "status": "PASS" if cgamma_open_ok else "FAIL", "detail": "c_Gamma parent zero is rejected and bound route active"})

    zero_law_ok = any(row["zero_law_id"] == "ZL4541_2_memory_not_inherited" and row["status"] == "ZERO_REJECTED_CURRENT_CORPUS" for row in zero_laws)
    checks.append({"validation_id": "VAL4541_03_no_piggyback", "status": "PASS" if zero_law_ok else "FAIL", "detail": "c_Gamma does not piggyback on c_D/delta_kappa zeros"})

    obstruction_ok = any(row["obstruction_id"] == "CGO4541_4_tensor" and row["status"] == "HARD_OBSTRUCTION" for row in obstructions)
    checks.append({"validation_id": "VAL4541_04_obstructions", "status": "PASS" if obstruction_ok else "FAIL", "detail": "homogeneous tensor obstruction retained"})

    bounds_ok = any(row["bound_id"] == "PB4541_0_master" for row in bounds) and any(row["bound_id"] == "PB4541_3_orbital" and row["status"] == "best_first_empirical_fallback" for row in bounds)
    checks.append({"validation_id": "VAL4541_05_bounds", "status": "PASS" if bounds_ok else "FAIL", "detail": "c_Gamma projection-bound route is active and orbital fallback selected"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    public_block = any(row["claim_gate_id"] == "CG4541_4_public_local_GR" and row["status"] == "BLOCKED_NONCLAIM" for row in gates)
    checks.append({"validation_id": "VAL4541_06_claim_firewall", "status": "PASS" if gates_ok and public_block else "FAIL", "detail": "all claim gates remain nonclaim"})

    csv_paths = [SOURCE_REGISTER, TRIPLE_AUDIT_CSV, ZERO_LAW_CSV, CGAMMA_OBSTRUCTION_CSV, PROJECTION_BOUND_CSV, CLAIM_GATES_CSV, DECISION_CSV, NEXT_CSV, STATUS_CSV]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4541_07_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4541_08_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4541_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4541 same-coframe/kappa/memory triple zero or projection bound"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    triple: list[dict[str, Any]],
    zero_laws: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4541 - same-coframe/kappa/memory triple zero under effective local branch or projection bound

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4540 named the priority triple:

```text
c_D, delta_kappa, c_Gamma.
```

4541 imports the strongest existing result instead of re-running the same maze:

```text
c_D = 0             inside PPC4161-GP-HQNP effective local branch,
delta_kappa = 0    inside PPC4161-GP-HQNP effective local branch,
c_Gamma != proven zero.
```

The important theorem is negative:

```text
c_D=0 and delta_kappa=0 do not imply c_Gamma=0.
```

`c_Gamma` is a separate memory-support/projector problem. Its zero requires parent ownership of verticality, compact support, boundary routing, bulk-source silence and homogeneous tensor no-hair. Current evidence does not close those clauses, so the honest branch is:

```text
|R_A^Gamma| <= |J_A^Gamma| |c_Gamma| ||P_A Gamma_mem||
             + |J_A^perp| ||Gamma_perp/K_perp||.
```

The best next move is a parent memory equation if possible; otherwise fill the first projection-bound row, preferably orbital/Gdot or PPN before R10.

## Triple Zero Audit

{markdown_table(triple)}

## Private Zero Laws

{markdown_table(zero_laws)}

## c_Gamma Obstruction Ledger

{markdown_table(obstructions)}

## c_Gamma Projection-Bound Route

{markdown_table(bounds)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_memory_residual",
        "claim": "4541 imports the current best triple-zero result: c_D and delta_kappa are private zeros inside the effective local branch, but c_Gamma parent zero is rejected and an explicit c_Gamma projection-bound route remains active.",
        "current_evidence": "Generated source register, triple audit, private zero laws, cGamma obstruction ledger, projection-bound route, claim gates, status and validation CSVs.",
        "status": "cD_deltaKappa_private_zero_cGamma_open_projection_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating local memory hair as solved just because metric/coframe and kappa/source drift are privately zero.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "c_Gamma needs parent memory equation or real projection-bound rows before local-GR/R10/PPN/clock/orbital claims.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    triple = triple_audit_rows()
    zero_laws = zero_law_rows()
    obstructions = cgamma_obstruction_rows()
    bounds = projection_bound_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TRIPLE_AUDIT_CSV, triple)
    write_csv(ZERO_LAW_CSV, zero_laws)
    write_csv(CGAMMA_OBSTRUCTION_CSV, obstructions)
    write_csv(PROJECTION_BOUND_CSV, bounds)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, triple, zero_laws, obstructions, bounds, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, triple, zero_laws, obstructions, bounds, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4541 Same-Coframe/Kappa/Memory Triple Zero Or Projection Bound

Marker: `{MARKER}`  
4541 imports the strongest existing triple-zero result into the current 4540 chain. Inside the effective `PPC4161-GP-HQNP` branch, `c_D=0` and `delta_kappa=0` privately. `c_Gamma` does not inherit those zeros and remains the active MTS-specific local memory coefficient. Its parent zero is rejected in the current corpus; the live route is a parent memory equation or an explicit projection-bound row. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4541 Packet Integration - cD/deltaKappa Private Zero, cGamma Open

Marker: `{PACKET_MARKER}`  
The packet now records the priority triple result: same-coframe leakage `c_D` and source drift `delta_kappa` are private zeros under the effective local branch, while local memory hair `c_Gamma` remains open and must be handled by parent memory support/no-hair proof or finite projection bounds.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
