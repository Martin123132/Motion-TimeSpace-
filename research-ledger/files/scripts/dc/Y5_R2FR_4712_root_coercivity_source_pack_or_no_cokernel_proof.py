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

CHECKPOINT = "4712"
CLAIM_ID = "L-554"
MARKER = "PPC4161_ROOT_COHERCIVITY_SOURCE_PACK_OR_NO_COKERNEL_PROOF_4712"
PACKET_MARKER = "PPC4161_PACKET_ROOT_COHERCIVITY_SOURCE_PACK_OR_NO_COKERNEL_PROOF_4712"
DECISION = "RQ_COKERNEL_SPLIT_AND_COERCIVE_GAP_LAW_DERIVED_SOURCE_PACK_VALUES_MISSING_NONCLAIM"
NEXT_TARGET = "4713-Y5-R2FR-no-linear-EM-owner-even-residual-symmetry-or-Llinear-bound.md"

DOC_PATH = POST / "4712-Y5-R2FR-root-coercivity-source-pack-or-no-cokernel-proof.md"
FORMAL_PATH = FORMAL / "728-PPC4161-root-coercivity-source-pack-or-no-cokernel-proof.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4711_ROOT = SOURCE_DIR / "P8_Y5_R2FR_4711_ROOT_NORMAL_EQUATION_CERTIFICATE.csv"
CSV_4711_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4711_FINITE_ROOT_CLOCK_INPUT_ROWS.csv"
CSV_4711_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4711_VALIDATION.csv"
CSV_4200_ENERGY = SOURCE_DIR / "P8_Y5_R2FR_4200_ENERGY_IDENTITY.csv"
CSV_4200_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_4200_BOUNDARY_INTERFACE.csv"
CSV_4202_LT = SOURCE_DIR / "P8_Y5_R2FR_4202_LT_DERIVATION.csv"
CSV_4202_CASES = SOURCE_DIR / "P8_Y5_R2FR_4202_COHERCIVITY_CASES.csv"
CSV_4202_PACK = SOURCE_DIR / "P8_Y5_R2FR_4202_FIRST_SOURCE_PACK.csv"
CSV_4302_GAP = SOURCE_DIR / "P8_Y5_R2FR_4302_COERCIVITY_GAP_DERIVATION.csv"
CSV_4302_PACK = SOURCE_DIR / "P8_Y5_R2FR_4302_SOURCE_BOUNDARY_INPUT_PACK.csv"
CSV_4311_ROUTES = SOURCE_DIR / "P8_Y5_R2FR_4311_POSITIVITY_ROUTE_AUDIT.csv"
CSV_4311_COMPONENTS = SOURCE_DIR / "P8_Y5_R2FR_4311_LAMBDA_COMPONENT_LEDGER.csv"
CSV_4311_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4311_COLLAR_RESIDUAL_FIRST_BOUND.csv"
CSV_4176_NOFLUX = SOURCE_DIR / "P8_Y5_R2FR_4176_NO_FLUX_THEOREM.csv"
CSV_4268_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_4268_BOUNDARY_PROJECTOR_THEOREM.csv"
CSV_3222_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_3222_PARENT_ACTION_DEFECT_NORM_CONTRACT.csv"
CSV_3222_GUARDS = SOURCE_DIR / "P8_Y5_R2FR_3222_STRESS_POYNTING_AND_READOUT_GUARDS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4712_SOURCE_REGISTER.csv"
COKERNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4712_COKERNEL_SPLIT_AND_GAP_THEOREM.csv"
SOURCE_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4712_ROOT_COHERCIVITY_SOURCE_PACK.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4712_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4712_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4712_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4712_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4712_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4712_VALIDATION.csv"


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
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
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
        ("SRC4712_00_4711_normal", CSV_4711_ROOT, "RNC4711_0_parent_residual_square_normal_equation", "4711 normal-equation handoff"),
        ("SRC4712_01_4711_finite", CSV_4711_ROOT, "RNC4711_1_finite_root_bound", "4711 finite root bound"),
        ("SRC4712_02_4711_inputs", CSV_4711_FINITE, "FRC4711_0_Croot", "4711 C_root source row"),
        ("SRC4712_03_4711_validation", CSV_4711_VALIDATION, "VAL4711_OVERALL", "4711 validation"),
        ("SRC4712_04_4200_energy", CSV_4200_ENERGY, "EI4200_2_coercivity", "energy identity coercivity analogue"),
        ("SRC4712_05_4200_zero", CSV_4200_ENERGY, "EI4200_3_zero_result", "energy identity zero result analogue"),
        ("SRC4712_06_4200_boundary", CSV_4200_BOUNDARY, "BI4200_2_energy_bridge", "boundary no-flux not enough firewall"),
        ("SRC4712_07_4202_operator", CSV_4202_LT, "OP4202_4_coercivity", "operator positivity and Poincare analogue"),
        ("SRC4712_08_4202_resolvent", CSV_4202_LT, "OP4202_5_resolvent", "finite resolvent analogue"),
        ("SRC4712_09_4202_cases", CSV_4202_CASES, "CASE4202_3_neumann_massless", "Neumann zero-mode failure case"),
        ("SRC4712_10_4202_pack", CSV_4202_PACK, "lambda_D", "spectral source-pack row"),
        ("SRC4712_11_4302_gap", CSV_4302_GAP, "CG4302_1_coercive_gap", "coercive gap formula"),
        ("SRC4712_12_4302_exact", CSV_4302_GAP, "CG4302_3_exact_nohair", "exact nohair theorem analogue"),
        ("SRC4712_13_4302_pack", CSV_4302_PACK, "IP4302_3_lambda1", "lambda1 source-pack analogue"),
        ("SRC4712_14_4311_dirichlet", CSV_4311_ROUTES, "PR4311_0_poincare_dirichlet", "Dirichlet/Poincare route"),
        ("SRC4712_15_4311_mass", CSV_4311_ROUTES, "PR4311_1_mass_only", "mass-only zero-mode route"),
        ("SRC4712_16_4311_components", CSV_4311_COMPONENTS, "LC4311_4_lambda_star", "lambda floor component ledger"),
        ("SRC4712_17_4311_bound", CSV_4311_BOUND, "RB4311_5_zero_case", "zero case with positive lambda"),
        ("SRC4712_18_4176_noflux", CSV_4176_NOFLUX, "NFT4176_5_no_flux_conclusion", "compact no-flux branch"),
        ("SRC4712_19_4268_boundary", CSV_4268_BOUNDARY, "BPROJ4268_2_no_flux_support", "fixed collar no-flux support"),
        ("SRC4712_20_3222_root", CSV_3222_CONTRACT, "DNC3222_2_same_branch_root", "same-branch root gap"),
        ("SRC4712_21_3222_stress", CSV_3222_GUARDS, "SPG3222_0_null_wave_guard", "EM stress/Poynting guard"),
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


def cokernel_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CK4712_0_cokernel_split",
            "claim_piece": "residual decomposition",
            "statement": "Decompose R_Q = Pi_coker R_Q + R_Q^perp, with R_Q^perp in the closed coercive range controlled by A_Q^dagger W.",
            "derivation": "The normal equation only sees A_Q^dagger W R_Q. Any component in ker(A_Q^dagger W) is a cokernel/harmonic residual and must be zeroed or bounded separately.",
            "result": "stationarity controls only R_Q^perp unless Pi_coker R_Q=0",
            "status": "EXACT_LINEAR_ALGEBRA_SPLIT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CK4712_1_RQ_gap_law",
            "claim_piece": "coercive root gap",
            "statement": "If the residual complex has kinetic lower bound Z_RQ_min>0, domain spectral gap lambda_1_RQ>=0, mass/Hessian floor M_RQ_min^2>=0, and negative correction bounded by Eta_RQ, then lambda_RQ := Z_RQ_min lambda_1_RQ + M_RQ_min^2 - Eta_RQ controls R_Q^perp.",
            "derivation": "This is the 4202/4302/4311 coercive-gap argument applied to the R_Q residual complex: <R_Q,L_RQ R_Q> >= lambda_RQ ||R_Q^perp||^2 after boundary/cokernel projection.",
            "result": "if lambda_RQ>0 then C_root <= 1/lambda_RQ on the projected branch",
            "status": "COERCIVE_GAP_LAW_DERIVED_COMPONENTS_UNSOURCED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CK4712_2_exact_root_criterion",
            "claim_piece": "R_Q exact root",
            "statement": "If lambda_RQ>0, Pi_coker R_Q=0, J_root=0 and B_root=0, stationarity implies R_Q=0.",
            "derivation": "From A_Q^dagger W R_Q + J_root + B_root=0, the homogeneous branch gives A_Q^dagger W R_Q=0. CK4712_0 removes the cokernel and CK4712_1 gives ||R_Q|| <= C_root*0.",
            "result": "R_Q=0",
            "status": "EXACT_CONDITIONAL_ROOT_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CK4712_3_finite_root_bound",
            "claim_piece": "finite R_Q if exact clauses fail",
            "statement": "If any forcing survives, ||R_Q|| <= ||Pi_coker R_Q|| + (||J_root||+||B_root||)/lambda_RQ when lambda_RQ>0.",
            "derivation": "Control the projected piece by the inverse gap and retain the cokernel piece additively with no cancellation.",
            "result": "explicit finite root source-pack law",
            "status": "FINITE_BOUND_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CK4712_4_valid_gap_cases",
            "claim_piece": "allowed gap routes",
            "statement": "Dirichlet/anchored residual domains can use lambda_1_RQ>0; Neumann/no-flux domains require either M_RQ_min^2>Eta_RQ or an explicit zero-mode/cokernel projector; hyperbolic/radiative branches cannot use the static elliptic inverse.",
            "derivation": "Specializes the 4202 cases and 4311 positivity audit to R_Q.",
            "result": "prevents Neumann massless zero-mode smuggling",
            "status": "ROUTE_CLASSIFICATION_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_pack_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_0_ZRQ",
            "symbol": "Z_RQ_min",
            "definition": "positive kinetic/inner-product lower bound of the R_Q residual complex",
            "required_law": "Z_RQ >= Z_RQ_min > 0",
            "source_or_value": "MISSING",
            "status": "MISSING_PARENT_KINETIC_OR_INNER_PRODUCT_CERTIFICATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_1_lambda1",
            "symbol": "lambda_1_RQ",
            "definition": "first positive domain eigenvalue/singular gap after gauge and cokernel projection",
            "required_law": "||D_RQ r||^2 >= lambda_1_RQ ||r||^2 on the projected local domain",
            "source_or_value": "MISSING",
            "status": "MISSING_DOMAIN_SPECTRAL_GAP_OR_PROJECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_2_M2",
            "symbol": "M_RQ_min^2",
            "definition": "mass/Hessian floor controlling residual zero modes",
            "required_law": "M_RQ^2 >= M_RQ_min^2",
            "source_or_value": "MISSING",
            "status": "MISSING_MASS_OR_HESSIAN_FLOOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_3_Eta",
            "symbol": "Eta_RQ",
            "definition": "negative correction budget from hidden, boundary, stress/readout and nonlinear terms",
            "required_law": "|negative correction| <= Eta_RQ ||R_Q||^2",
            "source_or_value": "MISSING",
            "status": "MISSING_CORRECTION_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_4_lambdaRQ",
            "symbol": "lambda_RQ",
            "definition": "coercive root gap",
            "required_law": "lambda_RQ = Z_RQ_min*lambda_1_RQ + M_RQ_min^2 - Eta_RQ > 0",
            "source_or_value": "FORMULA_DERIVED_VALUE_MISSING",
            "status": "SYMBOLIC_GAP_DERIVED_UNSOURCED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_5_Croot",
            "symbol": "C_root",
            "definition": "inverse coercive constant for the projected residual",
            "required_law": "C_root <= 1/lambda_RQ if lambda_RQ>0",
            "source_or_value": "FORMULA_DERIVED_VALUE_MISSING",
            "status": "SYMBOLIC_INVERSE_DERIVED_UNSOURCED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_6_Jroot",
            "symbol": "J_root",
            "definition": "linear/source forcing in the root normal equation",
            "required_law": "J_root=0 by parent no-linear-source theorem or finite norm source row",
            "source_or_value": "MISSING",
            "status": "MISSING_NO_LINEAR_SOURCE_THEOREM_OR_NORM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_7_Broot",
            "symbol": "B_root",
            "definition": "boundary forcing term in the root normal equation",
            "required_law": "B_root=0 under fixed compact no-flux collar, otherwise finite boundary norm",
            "source_or_value": "CONDITIONAL_NOFLUX_AVAILABLE_NOT_ADOPTED_FOR_RQ",
            "status": "BOUNDARY_BRANCH_CONDITIONAL_NEEDS_RQ_DOMAIN_MATCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_8_Picoker",
            "symbol": "Pi_coker R_Q",
            "definition": "harmonic/cokernel residual invisible to the normal equation",
            "required_law": "Pi_coker R_Q=0 or finite norm retained",
            "source_or_value": "MISSING",
            "status": "MISSING_NO_COKERNEL_PROOF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RCP4712_9_Llinear",
            "symbol": "L_linear",
            "definition": "linear EM kinetic owner leakage",
            "required_law": "L_linear=0 via even-residual symmetry/operator-domain exhaustion or finite derivative bound",
            "source_or_value": "MISSING",
            "status": "DEFERRED_TO_4713_NO_LINEAR_OWNER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4712_0_gap_positive",
            "required": "lambda_RQ = Z_RQ_min*lambda_1_RQ + M_RQ_min^2 - Eta_RQ > 0",
            "current_result": "BLOCKED_VALUES_MISSING",
            "if_pass": "projected residual inverse exists with C_root <= 1/lambda_RQ",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4712_1_cokernel_zero",
            "required": "Pi_coker R_Q=0 by gauge/domain/topology/no-harmonic theorem",
            "current_result": "BLOCKED_NO_COKERNEL_PROOF_MISSING",
            "if_pass": "stationarity can force full R_Q, not only projected R_Q",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4712_2_source_boundary_zero",
            "required": "J_root=B_root=0 on the same R_Q local branch",
            "current_result": "BLOCKED_RQ_DOMAIN_MATCH_MISSING",
            "if_pass": "homogeneous normal equation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4712_3_root_promote",
            "required": "GATE4712_0 + GATE4712_1 + GATE4712_2",
            "current_result": "BLOCKED_BY_UPSTREAM_GATES",
            "if_pass": "R_Q=0 can feed 4710 exact-root clock branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4712_0_no_neumann_zero_mode_smuggle",
            "rule": "No-flux/Neumann boundary conditions do not supply a positive gap unless a mass floor or zero-mode/cokernel projector is signed.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4712_1_no_boundary_equals_cokernel",
            "rule": "Boundary no-flux can set B_root=0 only on the matched R_Q domain; it does not prove Pi_coker R_Q=0.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4712_2_no_RQ_root_to_EM_stress_transfer",
            "rule": "Even a proven R_Q coefficient root must still pass the separate EM stress/Poynting/current-normalization gates before local-GR transfer.",
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
            "branch": "MTS_R2FR_Y5_RQ_COKERNEL_COERCIVITY_4712",
            "decision": DECISION,
            "reason": "4712 derives the exact cokernel split and positive-gap law needed by 4711. The branch is now a source-pack problem with lambda_RQ, Pi_coker, J_root and B_root named; no claim is promoted because values/theorems are still missing.",
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
            "derived": "cokernel split; lambda_RQ gap law; exact root criterion; finite root bound; source-pack rows",
            "not_derived": "numeric/theorem Z_RQ_min, lambda_1_RQ, M_RQ_min^2, Eta_RQ, Pi_coker zero, J_root/B_root zero, L_linear zero",
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
            "next_id": "NT4712_0",
            "target": NEXT_TARGET,
            "reason": "The root gap now has a source pack, but the exact-root clock branch still fails if the EM kinetic owner has a linear residual term; attack L_linear next.",
            "derive_first": "prove even-residual/no-linear EM owner or operator-domain exhaustion",
            "fallback": "source a finite L_linear hidden-Hom/readout derivative bound and propagate into the clock residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4712 - Root Coercivity Source Pack Or No-Cokernel Proof

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
4712 specializes the coercive-gap machinery to the `R_Q` residual complex.

The key split is:

```text
R_Q = Pi_coker R_Q + R_Q^perp
```

and the projected positive-gap law is:

```text
lambda_RQ := Z_RQ_min * lambda_1_RQ + M_RQ_min^2 - Eta_RQ
C_root <= 1/lambda_RQ       if lambda_RQ > 0.
```

Exact root criterion:

```text
lambda_RQ > 0
Pi_coker R_Q = 0
J_root = 0
B_root = 0
=> R_Q = 0.
```

Finite fallback:

```text
||R_Q|| <= ||Pi_coker R_Q|| + (||J_root|| + ||B_root||)/lambda_RQ.
```

This is a proper proof rung: no-flux is not confused with no-cokernel, and Neumann/no-flux zero modes are explicitly guarded.

## Source Register
{table(data["sources"])}

## Cokernel Split And Gap Theorem
{table(data["cokernel"])}

## Root Coercivity Source Pack
{table(data["source_pack"])}

## Promotion Gates
{table(data["promotion"])}

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
        f"""# 728 - PPC4161 Root Coercivity Source Pack Or No-Cokernel Proof

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Residual split:

```text
R_Q = Pi_coker R_Q + R_Q^perp.
```

Projected coercive gap:

```text
lambda_RQ = Z_RQ_min lambda_1_RQ + M_RQ_min^2 - Eta_RQ.
```

If `lambda_RQ>0`, then:

```text
||R_Q^perp|| <= (||J_root||+||B_root||)/lambda_RQ.
```

Full exact root requires:

```text
Pi_coker R_Q=0,
J_root=0,
B_root=0.
```

Therefore:

```text
R_Q=0.
```

No-flux collars can help with `B_root`, but they are not no-cokernel proofs. Neumann/no-flux branches need a mass floor or explicit zero-mode/cokernel projection.
""",
        encoding="utf-8",
    )


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fields = list(claims[0].keys()) if claims else [
        "claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk",
        "sector", "evidence", "next_action", "risk", "title", "notes",
    ]
    row = {field: "" for field in fields}
    row.update(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_empirical_interface",
            "claim": "4712 derives the R_Q cokernel split and positive coercive-gap source pack needed to promote the exact root theorem.",
            "current_evidence": "Generated source register, cokernel split/gap theorem rows, root coercivity source pack, promotion gates, firewalls, decision, status, next target and validation.",
            "status": "RQ_cokernel_gap_law_nonclaim_source_pack_missing",
            "next_test": NEXT_TARGET,
            "key_risk": "Treating no-flux as no-cokernel, or using a Neumann massless branch without zero-mode projection.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Root coercivity source pack or no-cokernel proof",
            "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
        }
    )
    existing = next((claim for claim in claims if claim.get("claim_id") == CLAIM_ID), None)
    if existing is None:
        claims.append(row)
    else:
        existing.update(row)
    write_csv(CLAIMS_PATH, claims)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: `R_Q` root control is now split into cokernel plus projected coercive branch.
- Gap law: `lambda_RQ = Z_RQ_min lambda_1_RQ + M_RQ_min^2 - Eta_RQ`; if positive, `C_root <= 1/lambda_RQ`.
- Exact root requires `Pi_coker R_Q=0`, `J_root=0`, and `B_root=0`; no-flux alone is not enough.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: specializes existing coercive-gap machinery to the `R_Q` residual complex and stages the source pack.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: 2026-07-07

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4712-Y5-R2FR-root-coercivity-source-pack-or-no-cokernel-proof.md`

## What Changed

The exact-root route now has a cokernel split:

```text
R_Q = Pi_coker R_Q + R_Q^perp
lambda_RQ = Z_RQ_min * lambda_1_RQ + M_RQ_min^2 - Eta_RQ
C_root <= 1/lambda_RQ if lambda_RQ > 0.
```

Exact root requires:

```text
lambda_RQ > 0, Pi_coker R_Q=0, J_root=0, B_root=0
=> R_Q=0.
```

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not treat no-flux as no-cokernel.
- Do not use a Neumann/no-flux branch without mass gap or zero-mode projection.
- Do not push to GitHub unless Martin explicitly asks for a GitHub update.
""",
        encoding="utf-8",
    )


def validation_rows(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False, "timestamp_utc": timestamp})

    add("VAL4712_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4712_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4712_2_cokernel_split", any(row["theorem_id"] == "CK4712_0_cokernel_split" for row in data["cokernel"]), "cokernel split theorem present")
    add("VAL4712_3_gap_law", any(row["theorem_id"] == "CK4712_1_RQ_gap_law" for row in data["cokernel"]), "lambda_RQ gap law present")
    add("VAL4712_4_exact_root", any(row["theorem_id"] == "CK4712_2_exact_root_criterion" for row in data["cokernel"]), "exact root criterion present")
    add("VAL4712_5_finite_bound", any(row["theorem_id"] == "CK4712_3_finite_root_bound" for row in data["cokernel"]), "finite root bound present")
    add("VAL4712_6_source_pack", len(data["source_pack"]) >= 10, "root source pack rows present")
    add("VAL4712_7_gates", len(data["promotion"]) >= 4, "promotion gates present")
    add("VAL4712_8_firewalls", len(data["firewalls"]) >= 3, "firewalls present")
    add("VAL4712_9_next_target", data["next"][0]["target"] == NEXT_TARGET, "4713 next target selected")
    add("VAL4712_10_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4712_11_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4712_12_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4712_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4712_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")
    add("VAL4712_15_resume_updated", NEXT_TARGET in text(RESUME_PATH), "resume bookmark updated")

    for csv_path in [SOURCE_REGISTER, COKERNEL_CSV, SOURCE_PACK_CSV, PROMOTION_CSV, FIREWALL_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4712_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4712_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for group in [data["cokernel"], data["source_pack"], data["promotion"], data["firewalls"], data["decision"], data["status"], data["next"]]:
        for row in group:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4712_16_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4712_17_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4712_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_status_next(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "cokernel": cokernel_rows(timestamp),
        "source_pack": source_pack_rows(timestamp),
        "promotion": promotion_rows(timestamp),
        "firewalls": firewall_rows(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(COKERNEL_CSV, data["cokernel"])
    write_csv(SOURCE_PACK_CSV, data["source_pack"])
    write_csv(PROMOTION_CSV, data["promotion"])
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
