from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4747"
CLAIM_ID = "L-589"
MARKER = "PPC4161_STATIC_GAP_CONSTANT_SOURCE_AND_OWNER_SYMBOL_COMPLETION_4747"
PACKET_MARKER = "PPC4161_PACKET_STATIC_GAP_CONSTANT_SOURCE_AND_OWNER_SYMBOL_COMPLETION_4747"
DECISION = "STATIC_GAP_CONSTANTS_SOURCE_READY_AND_OWNER_SYMBOLS_SCHEMATICALLY_COMPLETED_FULL_NUMERIC_GAP_STILL_BLOCKED_NONCLAIM"
NEXT_TARGET = "4748-Y5-R2FR-TT-quarantine-symbol-hardening-and-static-gap-smoke-runner.md"

DOC_PATH = POST / "4747-Y5-R2FR-static-gap-constant-source-and-owner-symbol-completion.md"
FORMAL_PATH = FORMAL / "763-PPC4161-static-gap-constant-source-and-owner-symbol-completion.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_SOURCE_REGISTER.csv"
STATIC_CONSTANTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_STATIC_GAP_CONSTANT_SOURCE_TABLE.csv"
POINCARE_CERTIFICATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_POINCARE_COLLAR_CERTIFICATE.csv"
DN_CONSTANT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_DN_CONSTANT_DEFINITION.csv"
OWNER_SYMBOL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_OWNER_SYMBOL_COMPLETION.csv"
BOUNDARY_COMPLEMENTING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_BOUNDARY_COMPLEMENTING_GATE.csv"
STATIC_SCORE_DRYRUN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_STATIC_SCORE_DRYRUN.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4747_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4747_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4747_0_4746_doc", POST / "4746-Y5-R2FR-static-PPN-elliptic-slice-gap-proof-or-lorentzian-energy-bound.md", "source c_DN, C_P, L_loc", "4747 handoff"),
    ("SRC4747_1_4746_formal", FORMAL / "762-PPC4161-static-PPN-elliptic-slice-gap-proof-or-lorentzian-energy-bound.md", "lambda_1^stat >= c_DN/(C_P L_loc^2)", "formal gap law"),
    ("SRC4747_2_4746_static_gap", SOURCE_DIR / "P8_Y5_R2FR_4746_STATIC_GAP_PROOF.csv", "SGP4746_3_gap_bound", "static gap law"),
    ("SRC4747_3_4746_owner", SOURCE_DIR / "P8_Y5_R2FR_4746_OWNER_SYMBOL_COMPLETION_LEDGER.csv", "OWN4746_1_TT", "owner symbols missing"),
    ("SRC4747_4_4746_residual", SOURCE_DIR / "P8_Y5_R2FR_4746_RESIDUAL_BOUND_LAW.csv", "RB4746_0_static", "static residual law"),
    ("SRC4747_5_4746_operator", SOURCE_DIR / "P8_Y5_R2FR_4746_STATIC_OPERATOR_SETUP.csv", "STATOP4746_4_laplacian", "static operator"),
    ("SRC4747_6_4746_arena", SOURCE_DIR / "P8_Y5_R2FR_4746_STATIC_TEST_ARENA_MAPPING.csv", "ARENA4746_0_PPN", "static arena mapping"),
    ("SRC4747_7_4745_symbols", SOURCE_DIR / "P8_Y5_R2FR_4745_ADJOINT_PRINCIPAL_SYMBOL_DERIVATION.csv", "SYM4745_6_missing_full_owner_symbol", "symbol gap"),
    ("SRC4747_8_4745_DN", SOURCE_DIR / "P8_Y5_R2FR_4745_DN_ELLIPTICITY_UCP_GATE.csv", "DN4745_5_full_owner_gate", "full owner gate"),
    ("SRC4747_9_4744_boundary", SOURCE_DIR / "P8_Y5_R2FR_4744_ADMISSIBLE_MULTIPLIER_SPACE.csv", "ADM4744_1_trace_domain", "H1_0 boundary domain"),
    ("SRC4747_10_4740_action", SOURCE_DIR / "P8_Y5_R2FR_4740_PARENT_TFRI_OWNER_ACTION_BLOCK.csv", "S_TT = int sqrt|g|", "TT owner action"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    STATIC_CONSTANTS_CSV,
    POINCARE_CERTIFICATE_CSV,
    DN_CONSTANT_CSV,
    OWNER_SYMBOL_CSV,
    BOUNDARY_COMPLEMENTING_CSV,
    STATIC_SCORE_DRYRUN_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def static_constant_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CONST4747_0_Lloc",
            "L_loc",
            "diam_h(Sigma_loc)",
            "length",
            "source from parent-fixed static collar geometry",
            "SOURCE_READY_GEOMETRY_REQUIRED",
        ),
        (
            "CONST4747_1_CP_canonical",
            "C_P",
            "1/pi^2 for canonical interval/box/radial Dirichlet collar after L_loc normalization",
            "dimensionless",
            "conditional canonical value; general collar must source its own Poincare constant",
            "CONDITIONAL_CANONICAL_VALUE",
        ),
        (
            "CONST4747_2_cDN",
            "c_DN",
            "inf_{x,p,m} ||sigma_DN(D_stat)(x,p)m||^2/(|p|_h^2 ||m||^2) on unit spatial cotangent and M_adm",
            "dimensionless",
            "source from full TFRI+TT+quarantine DN symbol after all parent components are fixed",
            "SOURCE_READY_SYMBOL_REQUIRED",
        ),
        (
            "CONST4747_3_Piowner",
            "Pi_owner^stat",
            "operator norm from static multiplier amplitude to PPN/R10/clock/orbital readout",
            "dimensionless",
            "source per arena after readout projection is fixed",
            "SOURCE_READY_ARENA_REQUIRED",
        ),
        (
            "CONST4747_4_gap",
            "lambda_1^stat",
            ">= c_DN/(C_P L_loc^2)",
            "1/length^2",
            "derived from 4746 once c_DN,C_P,L_loc are sourced",
            "DERIVED_SOURCE_READY_FORMULA",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "constant_id": constant_id,
            "symbol": symbol,
            "definition_or_value": definition,
            "units": units,
            "source_rule": source_rule,
            "status": status,
            "numeric_value": "MISSING_UNLESS_CONDITIONAL_CANONICAL",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for constant_id, symbol, definition, units, source_rule, status in specs
    ]


def poincare_certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PC4747_0_domain",
            "m in H^1_0(Sigma_loc,E_m)",
            "Dirichlet trace from parent boundary contract.",
            "SOURCE_BACKED_BY_4744",
        ),
        (
            "PC4747_1_geometry",
            "L_loc := diam_h(Sigma_loc)",
            "Normalizes the collar size for the Poincare bound.",
            "GEOMETRY_SOURCE_REQUIRED",
        ),
        (
            "PC4747_2_general_bound",
            "||m||^2 <= C_P L_loc^2 ||nabla_h m||^2",
            "General collar Poincare inequality; C_P is sourceable once the collar shape is fixed.",
            "DERIVED_FORM",
        ),
        (
            "PC4747_3_canonical_bound",
            "C_P=1/pi^2 for canonical one-dimensional/box/radial Dirichlet collar normalization",
            "Useful smoke value, not a general-geometry claim.",
            "CONDITIONAL_CANONICAL_ONLY",
        ),
        (
            "PC4747_4_firewall",
            "if Sigma_loc geometry is not fixed then C_P remains MISSING_DOMAIN_GEOMETRY",
            "Prevents using a pretty constant on an unspecified collar.",
            "FIREWALL",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": certificate_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, formula, meaning, status in specs
    ]


def dn_constant_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "DNK4747_0_definition",
            "c_DN := inf ||sigma_DN(D_stat)(x,p)m||^2/(|p|_h^2||m||^2)",
            "The exact constant needed for the gap law.",
            "DEFINITION",
        ),
        (
            "DNK4747_1_TFRI_subblock",
            "c_TFRI from sigma_R,sigma_Gamma,sigma_phi on the TFRI multiplier subspace",
            "TFRI-only symbol exists but cannot certify the full owner operator.",
            "PARTIAL_PRESENT",
        ),
        (
            "DNK4747_2_TT_subblock",
            "c_TT from sigma_TT(k;xi)",
            "Needs exact DeltaK/TT owner parent field and projector.",
            "SCHEMATIC_PRESENT_NOT_NUMERIC",
        ),
        (
            "DNK4747_3_quarantine_subblock",
            "c_quar from sigma_quar(k;chi)",
            "Needs exact q_tr/K_own parent field map.",
            "SCHEMATIC_PRESENT_NOT_NUMERIC",
        ),
        (
            "DNK4747_4_full_constant",
            "c_DN >= min(c_TFRI,c_TT,c_quar)-C_mix",
            "Mixed block coupling must be bounded before numeric scoring.",
            "DERIVED_SYMBOLIC_BOUND",
        ),
        (
            "DNK4747_5_blocker",
            "numeric c_DN requires c_TT,c_quar,C_mix and boundary complementing data",
            "This is the shortest source list for the static gap.",
            "MISSING_SOURCE_VALUES",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "dn_id": dn_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for dn_id, formula, meaning, status in specs
    ]


def owner_symbol_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "OWNC4747_0_TFRI",
            "sigma_TFRI(k)m = {sigma_R, sigma_Gamma, sigma_phi}",
            "TFRI symbol spine from 4745.",
            "PRESENT_FROM_4745",
        ),
        (
            "OWNC4747_1_TT",
            "sigma_TT(k;xi) = Pi_TT^*(k) i k_mu P_loc^* xi_nu plus projector/readout lower blocks",
            "Adjoint symbol of xi_nu P_loc nabla_mu Pi_TT[U]^{mu nu}; exact value needs parent TT field U and projector.",
            "SCHEMATIC_COMPLETION",
        ),
        (
            "OWNC4747_2_quarantine",
            "sigma_quar(k;chi) = i k_mu chi_nu on K_own^{mu nu} plus algebraic chi_nu on q_tr^nu",
            "Adjoint symbol of chi_nu(q_tr^nu+nabla_mu K_own^{mu nu}); exact value needs parent q_tr/K_own map.",
            "SCHEMATIC_COMPLETION",
        ),
        (
            "OWNC4747_3_projector",
            "sigma(P_loc), sigma(Pi_TT), sigma(Q_perp) must be fixed before c_DN is scored",
            "Projectors are part of the principal symbol if they are nonlocal/pseudodifferential.",
            "PROJECTOR_SOURCE_REQUIRED",
        ),
        (
            "OWNC4747_4_gap_block",
            "full sigma_DN(D_stat) = sigma_TFRI direct-sum sigma_TT direct-sum sigma_quar plus C_mix",
            "Owner-symbol completion is schematic but no longer blank.",
            "FULL_SYMBOL_SKELETON_WRITTEN",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "owner_symbol_id": owner_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for owner_id, formula, meaning, status in specs
    ]


def boundary_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("BC4747_0_domain", "H^1_0 static collar boundary", "Dirichlet trace condition is compatible with first-order/static blocks only after boundary symbol check.", "CONDITIONAL"),
        ("BC4747_1_TFRI", "TFRI boundary complementing symbol", "partly covered by H^1_0 trace plus trace-free Hessian order; exact mixed-order check remains.", "MIXED_ORDER_CHECK_REQUIRED"),
        ("BC4747_2_TT", "TT/superpotential boundary complementing symbol", "missing until sigma_TT and projector boundary behavior are fixed.", "MISSING_PARENT_COMPONENT"),
        ("BC4747_3_quarantine", "quarantine boundary complementing symbol", "missing until q_tr/K_own boundary behavior is fixed.", "MISSING_PARENT_COMPONENT"),
        ("BC4747_4_strong_route", "H^2_0 or compact support collar", "safe upgrade if normal-derivative boundary flux appears.", "OPTIONAL_STRONG_ROUTE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "boundary_id": boundary_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for boundary_id, condition, meaning, status in specs
    ]


def static_score_dryrun_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "DRY4747_0_symbolic_gap",
            "lambda_1^stat >= c_DN/(C_P L_loc^2)",
            "NOT_NUMERIC",
            "PASS_SYMBOLIC_ONLY",
            "Needs c_DN,C_P,L_loc.",
        ),
        (
            "DRY4747_1_canonical_CP_only",
            "C_P=1/pi^2, L_loc=MISSING, c_DN=MISSING",
            "NOT_SCORE_READY",
            "FAIL_CLOSED",
            "Canonical C_P alone cannot score anything.",
        ),
        (
            "DRY4747_2_missing_TT",
            "sigma_TT schematic but not parent-fixed",
            "NOT_SCORE_READY",
            "FAIL_CLOSED",
            "Write exact TT owner field/projector symbol.",
        ),
        (
            "DRY4747_3_missing_quar",
            "sigma_quar schematic but not parent-fixed",
            "NOT_SCORE_READY",
            "FAIL_CLOSED",
            "Write exact q_tr/K_own symbol.",
        ),
        (
            "DRY4747_4_static_residual",
            "C_res_static <= Pi_owner^stat sqrt(CzeroMode_stat^2+(C_Dstat^2+C_boundary_stat) C_P L_loc^2/c_DN)",
            "SYMBOLIC_NONCLAIM",
            "NOT_SCORE_READY",
            "Source all constants before any PPN/R10 claim.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "dryrun_id": dryrun_id,
            "case": case,
            "value_state": value_state,
            "result": result,
            "next_action": next_action,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for dryrun_id, case, value_state, result, next_action in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4747_0_harden_TT_quar", "turn schematic sigma_TT/sigma_quar into exact parent-owned symbols", "best_next_route", "unblocks c_DN source path"),
        ("ROUTE4747_1_static_gap_smoke", "build a toy static collar gap smoke runner with canonical C_P", "parallel_smoke_route", "tests pipeline but not claim-ready"),
        ("ROUTE4747_2_geometry_source", "choose/source Sigma_loc geometry and L_loc", "parallel_source_route", "needed for any numeric gap"),
        ("ROUTE4747_3_score_now", "score PPN/R10 using symbolic constants", "rejected", "not score-ready"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "reason_or_next_requirement": requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, requirement in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4747_0_sources", "All cited 4747 source anchors exist and contain expected text.", "pass_internal", False),
        ("GATE4747_1_constants", "L_loc,C_P,c_DN,Pi_owner have source-ready definitions.", "conditional_pass", False),
        ("GATE4747_2_CP", "Canonical C_P=1/pi^2 is allowed only for canonical collar smoke, not general claim.", "conditional_open", False),
        ("GATE4747_3_owner_symbols", "sigma_TT and sigma_quar are schematic, not exact parent-owned symbols.", "closed_unsigned", False),
        ("GATE4747_4_boundary", "Boundary complementing symbols remain incomplete.", "closed_unsigned", False),
        ("GATE4747_5_score", "Static score dryrun remains fail-closed until constants and symbols are sourced.", "closed_unsigned", False),
        ("GATE4747_6_no_claim", "No local-GR, Newton, PPN, R10, WEP, clock or orbital claim from 4747.", "closed_firewall", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, valid_for_claim in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4747_0_no_canonical_overclaim", "C_P=1/pi^2 is a canonical-collar smoke value only until Sigma_loc geometry is fixed."),
        ("FW4747_1_no_schematic_symbol_claim", "sigma_TT/sigma_quar schematic forms do not certify full owner ellipticity."),
        ("FW4747_2_no_symbolic_scoring", "Do not score PPN/R10/clock/orbital tests from symbolic constants."),
        ("FW4747_3_no_projector_hide", "P_loc/Pi_TT/Q_perp projector symbols must be fixed before c_DN is numeric."),
        ("FW4747_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "summary": "4747 turns the static gap constants into source-ready definitions, gives a conditional canonical Poincare smoke value, and writes schematic sigma_TT/sigma_quar owner symbols. The static residual remains fail-closed until geometry, projector symbols, exact owner symbols and constants are sourced.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4747_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4747_1_science_verdict",
            "status": "constants_source_ready_owner_symbols_schematic_score_blocked",
            "detail": "The static gap now has source-ready constants and owner-symbol skeletons, but exact sigma_TT/sigma_quar and geometry/projector constants are still required.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4747 leaves the shortest blockers as exact TT/quarantine owner symbols and a static gap smoke runner.",
            "preferred_route": "Harden sigma_TT and sigma_quar from schematic symbols into parent-owned operator symbols.",
            "fallback_route": "Build a canonical-collar static gap smoke runner that stays explicitly nonclaim.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    constants: list[dict[str, Any]],
    poincare: list[dict[str, Any]],
    dn_rows: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4747 Y5 R2FR: Static Gap Constant Source And Owner Symbol Completion

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint makes the 4746 static gap law sourceable:

```text
lambda_1^stat >= c_DN/(C_P L_loc^2)
L_loc = diam_h(Sigma_loc)
C_P = 1/pi^2 only for canonical Dirichlet collar smoke tests
c_DN = inf ||sigma_DN(D_stat)m||^2/(|p|_h^2||m||^2)
```

- It also writes schematic owner symbols for the previously blank TT/quarantine blocks:

```text
sigma_TT(k;xi) = Pi_TT^*(k) i k_mu P_loc^* xi_nu + projector terms
sigma_quar(k;chi) = i k_mu chi_nu on K_own^{{mu nu}} + algebraic chi_nu on q_tr^nu
```

- These are not claim-ready. They become useful because the next missing objects are now exact: parent field maps, projector symbols, boundary complementing symbols, and static collar geometry.

## Static Gap Constant Source Table

{bullet(constants, "constant_id", "symbol")}

## Poincare Collar Certificate

{bullet(poincare, "certificate_id", "formula")}

## DN Constant Definition

{bullet(dn_rows, "dn_id", "formula")}

## Owner Symbol Completion

{bullet(owners, "owner_symbol_id", "formula")}

## Boundary Complementing Gate

{bullet(boundary, "boundary_id", "condition")}

## Static Score Dryrun

{bullet(dryrun, "dryrun_id", "result")}

## Route Matrix

{bullet(routes, "route_id", "route")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 763 PPC4161: Static Gap Constant Source And Owner Symbol Completion

Generated: `{timestamp}`

## Sourceable Static Gap

4747 turns the static gap into source-ready quantities:

```text
lambda_1^stat >= c_DN/(C_P L_loc^2),
L_loc=diam_h(Sigma_loc),
c_DN=inf ||sigma_DN(D_stat)m||^2/(|p|_h^2||m||^2).
```

`C_P=1/pi^2` is carried only as a canonical Dirichlet-collar smoke value. General collars must source `C_P` from their actual geometry.

## Owner Symbol Skeletons

```text
sigma_TT(k;xi) = Pi_TT^*(k) i k_mu P_loc^* xi_nu + projector terms
sigma_quar(k;chi) = i k_mu chi_nu on K_own^{{mu nu}} + algebraic chi_nu on q_tr^nu.
```

These harden the missing owner symbols from blank placeholders into parent-symbol targets, but they remain schematic until the exact `U`, `Pi_TT`, `P_loc`, `q_tr`, and `K_own` maps are fixed.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4747 defines source-ready static gap constants: `L_loc=diam_h(Sigma_loc)`, `C_P`, `c_DN`, and `Pi_owner^stat`.
- It records `C_P=1/pi^2` only as a canonical Dirichlet-collar smoke value, not a general claim.
- It writes schematic owner symbols `sigma_TT(k;xi)` and `sigma_quar(k;chi)` so the missing full-owner pieces are no longer blank.
- Static scoring remains fail-closed until exact owner symbols, projector symbols, geometry and constants are sourced.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4747 local packet update: static gap constants are source-ready and TT/quarantine owner symbols are sketched. Next is hardening those symbols or running a clearly nonclaim canonical static-gap smoke test.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4747-Y5-R2FR-static-gap-constant-source-and-owner-symbol-completion.md`

## Decision

`{DECISION}`

## What moved forward

- Converted the static gap law into source-ready constants: `L_loc=diam_h(Sigma_loc)`, `C_P`, `c_DN`, and `Pi_owner^stat`.
- Kept `C_P=1/pi^2` only as a canonical Dirichlet-collar smoke value.
- Wrote schematic `sigma_TT` and `sigma_quar` owner symbols from the parent owner action forms.
- Static residual scoring remains fail-closed until exact owner symbols, projector symbols, geometry and constants are sourced.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_newton_bridge",
        "4747 makes the static gap constants source-ready and schematically completes the TT/quarantine owner symbols without opening a local-test claim.",
        "Generated source register, static constant table, Poincare certificate, DN constant definition, owner symbol completion, boundary complementing gate, static score dryrun, route matrix, gates, firewalls, decision, status, next target and validation.",
        "static_gap_constants_source_ready_owner_symbols_schematic_nonclaim",
        NEXT_TARGET,
        "Using canonical C_P or schematic owner symbols as if they were sourced constants/exact parent symbols.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need exact sigma_TT/sigma_quar, projector symbols, c_DN,C_P,L_loc,Pi_owner and boundary complementing data before scoring.",
        "Static gap constant source and owner symbol completion",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    constants: list[dict[str, Any]],
    poincare: list[dict[str, Any]],
    dn_rows: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4747_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4747_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4747_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4747_2_constants", "constants include L_loc,C_P,c_DN,Pi_owner", all(any(symbol in row["symbol"] for row in constants) for symbol in ["L_loc", "C_P", "c_DN", "Pi_owner"]), str(STATIC_CONSTANTS_CSV)))
    checks.append(("VAL4747_3_canonical_CP_firewall", "Poincare rows include canonical C_P and general-geometry firewall", any("1/pi^2" in row["formula"] for row in poincare) and any(row["status"] == "FIREWALL" for row in poincare), str(POINCARE_CERTIFICATE_CSV)))
    checks.append(("VAL4747_4_DN_bound", "DN rows include full c_DN symbolic bound and missing sources", any("min(c_TFRI,c_TT,c_quar)-C_mix" in row["formula"] for row in dn_rows) and any(row["status"] == "MISSING_SOURCE_VALUES" for row in dn_rows), str(DN_CONSTANT_CSV)))
    checks.append(("VAL4747_5_owner_symbols", "owner symbol rows contain sigma_TT and sigma_quar schematic completion", any("sigma_TT" in row["formula"] and row["status"] == "SCHEMATIC_COMPLETION" for row in owners) and any("sigma_quar" in row["formula"] and row["status"] == "SCHEMATIC_COMPLETION" for row in owners), str(OWNER_SYMBOL_CSV)))
    checks.append(("VAL4747_6_boundary_gate", "boundary gate keeps TT/quarantine complementing symbols missing", all(any(symbol in row["condition"] and row["status"] == "MISSING_PARENT_COMPONENT" for row in boundary) for symbol in ["TT", "quarantine"]), str(BOUNDARY_COMPLEMENTING_CSV)))
    checks.append(("VAL4747_7_dryrun_fail_closed", "static dryrun remains fail closed for missing exact symbols", all(row["result"] == "FAIL_CLOSED" for row in dryrun if row["dryrun_id"] in {"DRY4747_2_missing_TT", "DRY4747_3_missing_quar"}), str(STATIC_SCORE_DRYRUN_CSV)))
    checks.append(("VAL4747_8_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4747_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4747_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4747_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4747_12_claim_row", "claim row L-589 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4747_13_resume", "resume points from 4747 to 4748", "4747-Y5" in resume_text and "4748-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4747_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(item[2] for item in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4747_OVERALL",
            "check": "all 4747 local generation and nonclaim checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    constants = static_constant_rows(timestamp)
    poincare = poincare_certificate_rows(timestamp)
    dn_rows = dn_constant_rows(timestamp)
    owners = owner_symbol_rows(timestamp)
    boundary = boundary_gate_rows(timestamp)
    dryrun = static_score_dryrun_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(STATIC_CONSTANTS_CSV, constants)
    write_csv(POINCARE_CERTIFICATE_CSV, poincare)
    write_csv(DN_CONSTANT_CSV, dn_rows)
    write_csv(OWNER_SYMBOL_CSV, owners)
    write_csv(BOUNDARY_COMPLEMENTING_CSV, boundary)
    write_csv(STATIC_SCORE_DRYRUN_CSV, dryrun)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, constants, poincare, dn_rows, owners, boundary, dryrun, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, constants, poincare, dn_rows, owners, boundary, dryrun, gates, timestamp))


if __name__ == "__main__":
    main()
