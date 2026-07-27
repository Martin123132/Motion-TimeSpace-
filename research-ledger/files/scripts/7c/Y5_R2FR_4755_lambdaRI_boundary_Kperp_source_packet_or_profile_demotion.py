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

CHECKPOINT = "4755"
CLAIM_ID = "L-597"
MARKER = "PPC4161_LAMBDARI_BOUNDARY_KPERP_SOURCE_PACKET_OR_PROFILE_DEMOTION_4755"
PACKET_MARKER = "PPC4161_PACKET_LAMBDARI_BOUNDARY_KPERP_SOURCE_PACKET_OR_PROFILE_DEMOTION_4755"
DECISION = "PRIVATE_STATIC_OWNER_PACKET_CONDITIONALLY_CLEAN_SOURCE_CHARGE_COUPLING_GATE_NEXT_NONCLAIM"
NEXT_TARGET = "4756-Y5-R2FR-Htau-MHref-kappa-source-coupling-lock-or-transition-hair-bound.md"

DOC_PATH = POST / "4755-Y5-R2FR-lambdaRI-boundary-Kperp-source-packet-or-profile-demotion.md"
FORMAL_PATH = FORMAL / "771-PPC4161-lambdaRI-boundary-Kperp-source-packet-or-profile-demotion.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_SOURCE_REGISTER.csv"
OWNER_PACKET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_OWNER_PACKET_RESOLUTION.csv"
BRANCH_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_BRANCH_VERDICT.csv"
FINITE_PROFILE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_FINITE_PROFILE_DEMOTION_ROWS.csv"
SOURCE_COUPLING_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_SOURCE_CHARGE_COUPLING_IMPORT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4755_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4755_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4755_0_4754_doc", POST / "4754-Y5-R2FR-KGamma-owner-adoption-or-cancellation-angle-bound.md", "Adjoint-Zero Source Packet", "4754 source-packet handoff"),
    ("SRC4755_1_4754_formal", FORMAL / "770-PPC4161-KGamma-owner-adoption-or-cancellation-angle-bound.md", "L_RI^dagger Lambda = 0", "4754 owner metric silence condition"),
    ("SRC4755_2_4754_packet", SOURCE_DIR / "P8_Y5_R2FR_4754_ADJOINT_ZERO_SOURCE_PACKET.csv", "ADJPK4754_0_lambda_RI", "4754 lambda packet row"),
    ("SRC4755_3_4754_next", SOURCE_DIR / "P8_Y5_R2FR_4754_NEXT_TARGET.csv", "lambda_RI", "4755 handoff"),
    ("SRC4755_4_4350_gap", SOURCE_DIR / "P8_Y5_R2FR_4350_GAP_ROWS.csv", "GAP4350_0_clean_static", "lambda_RI clean gap"),
    ("SRC4755_5_4350_anchor", SOURCE_DIR / "P8_Y5_R2FR_4350_BOUNDARY_ANCHOR_ROWS.csv", "ANCH4350_0_parent_test_space", "RI boundary anchor"),
    ("SRC4755_6_4351_bound", SOURCE_DIR / "P8_Y5_R2FR_4351_OWNER_TAIL_BOUND_ROWS.csv", "BND4351_0_clean_zero", "owner-tail zero/fallback law"),
    ("SRC4755_7_4352_boundary", SOURCE_DIR / "P8_Y5_R2FR_4352_BOUNDARY_SILENCE_ROWS.csv", "BRI4352_3_boundary_zero_theorem", "boundary zero theorem"),
    ("SRC4755_8_4352_incoming", SOURCE_DIR / "P8_Y5_R2FR_4352_NO_INCOMING_ROWS.csv", "IRI4352_3_no_incoming_theorem", "incoming zero theorem"),
    ("SRC4755_9_4352_tail", SOURCE_DIR / "P8_Y5_R2FR_4352_FINITE_TAIL_VALUE_ROWS.csv", "TAIL4352_0_full_clean", "finite-tail fallback table"),
    ("SRC4755_10_4353_owner", SOURCE_DIR / "P8_Y5_R2FR_4353_OWNER_CHANNEL_ROWS.csv", "OC4353_4_owner_total", "owner-tail/Kperp deletion"),
    ("SRC4755_11_4353_vector", SOURCE_DIR / "P8_Y5_R2FR_4353_RESIDUAL_VECTOR_ROWS.csv", "RV4353_0_clean_private", "clean private residual vector"),
    ("SRC4755_12_4353_gates", SOURCE_DIR / "P8_Y5_R2FR_4353_REMAINING_GATE_ROWS.csv", "G4353_1_source_charge", "remaining source charge gate"),
    ("SRC4755_13_4354_charge", SOURCE_DIR / "P8_Y5_R2FR_4354_SOURCE_CHARGE_ROWS.csv", "SC4354_1_Htau_MHref", "source charge fork"),
    ("SRC4755_14_4354_coupling", SOURCE_DIR / "P8_Y5_R2FR_4354_COUPLING_LOCK_ROWS.csv", "CL4354_3_Gcal", "calibrated coupling lock"),
    ("SRC4755_15_4354_newton", SOURCE_DIR / "P8_Y5_R2FR_4354_NEWTON_BRIDGE_ROWS.csv", "NB4354_4_conditional_theorem", "Newton bridge theorem"),
    ("SRC4755_16_4354_drift", SOURCE_DIR / "P8_Y5_R2FR_4354_DRIFT_BOUND_ROWS.csv", "DB4354_6_MHref", "source/coupling drift bounds"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    OWNER_PACKET_CSV,
    BRANCH_VERDICT_CSV,
    FINITE_PROFILE_CSV,
    SOURCE_COUPLING_IMPORT_CSV,
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


def owner_packet_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("OP4755_0_lambda_clean", "lambda_4350 = pi^2/ell_RI^2", "compact anchored RI residual collar, Eta_RI=0, Dirichlet/test-space branch", "CONDITIONAL_POSITIVE_PRIVATE_GAP"),
        ("OP4755_1_lambda_bound", "lambda_4350 = pi^2/ell_RI^2 - Eta_RI,total_bound", "finite correction branch with 0 <= Eta_RI,total_bound < pi^2/ell_RI^2", "FORMULA_READY_VALUES_MISSING"),
        ("OP4755_2_boundary_zero", "B_Lambda=B_RI=0", "Lambda trace killed, domain fixed, boundary terms exact/routed in same collar", "CONDITIONAL_ZERO_IF_BRANCH_SIGNED"),
        ("OP4755_3_incoming_zero", "I_RI=0", "stationary isolated compact branch with no independent incoming RI datum", "CONDITIONAL_ZERO_IF_BRANCH_SIGNED"),
        ("OP4755_4_residual_zero", "R_Lambda=0", "exact adjoint equation in the clean RI owner branch", "CONDITIONAL_ZERO_IF_BRANCH_SIGNED"),
        ("OP4755_5_Kperp_zero", "Y_Kperp=0", "private compact selector routes Kperp into GR TT/vertical/boundary or no-extra-source sectors", "CONDITIONAL_PRIVATE_ZERO"),
        ("OP4755_6_owner_channel", "epsilon_owner_tail_Kperp=0", "lambda, boundary, incoming, residual and Kperp clauses close on the same private branch", "CHANNEL_DELETED_FROM_CLEAN_PRIVATE_VECTOR"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "packet_id": packet_id,
            "formula": formula,
            "condition": condition,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for packet_id, formula, condition, status in specs
    ]


def branch_verdict_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "BV4755_0_clean_private",
            "private compact static selector",
            "owner-tail/Kperp channel deleted",
            "Delta_local_after_owner = Delta_nonowner_remaining",
            "CONDITIONAL_PRIVATE_CLEAN_BRANCH",
        ),
        (
            "BV4755_1_finite_private",
            "private imperfect owner branch",
            "finite owner-tail/Kperp score retained",
            "Delta_local_after_owner <= Delta_nonowner_remaining + owner_tail_bound + Kperp_bound",
            "FINITE_VALUES_MISSING",
        ),
        (
            "BV4755_2_public_global",
            "public/global MTS",
            "owner-tail/Kperp not deleted without global parent signatures",
            "Delta_local_public retains owner-tail/Kperp plus nonowner gates",
            "PUBLIC_PROMOTION_BLOCKED",
        ),
        (
            "BV4755_3_next_gate",
            "post-owner local GR/Newton route",
            "source charge and calibrated coupling are now the next bottleneck",
            "H_tau/M_Hdress and kappa_eff/G_cal gates must close before Newton source law",
            "SOURCE_COUPLING_NEXT",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "verdict_id": verdict_id,
            "branch": branch,
            "owner_channel_status": status_text,
            "local_vector": local_vector,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for verdict_id, branch, status_text, local_vector, status in specs
    ]


def finite_profile_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FP4755_0_owner_tail", "Y_owner_a <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350 + |Pi_a^BRI||B_RI| + |Pi_a^I||I_RI|", "used if Lambda/boundary/incoming/residual clauses are unsigned", "VALUES_MISSING"),
        ("FP4755_1_Kperp", "Y_Kperp_i = |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)", "used if Kperp clean sector placement is unsigned", "VALUES_MISSING"),
        ("FP4755_2_total_owner", "epsilon_owner_tail_Kperp <= Y_owner_a + Y_Kperp_a", "finite owner-channel demotion if clean branch not signed", "NONCLAIM_PROFILE_ROW_READY"),
        ("FP4755_3_profile_demotion", "if any packet clause is unsigned and no source value exists, demote KGamma rescue to finite profile/closure-only", "prevents clean private branch from being treated as public theorem", "FAIL_CLOSED_RULE"),
        ("FP4755_4_no_cancellation", "finite owner profile cannot be canceled against nonowner residuals", "keeps empirical scoring honest", "ANTI_CANCELLATION_RULE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "profile_id": profile_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for profile_id, formula, meaning, status in specs
    ]


def source_coupling_import_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SCI4755_0_source_charge", "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref", "Hamiltonian/Hilbert source charge definition for Newtonian mass", "DEFINED_NOT_PUBLICLY_CLOSED"),
        ("SCI4755_1_worldtube", "int_W rho_H dV_H = M_H^dress[W_H;tau]", "same-worldtube Hilbert source measure must match the Hamiltonian charge", "CONDITION_REQUIRED"),
        ("SCI4755_2_kappa_eff", "kappa_eff = kappa_* Z_H", "effective local source coupling must be source-blind", "DERIVED_IF_COMPONENT_LOCKS_CLOSE"),
        ("SCI4755_3_Gcal", "G_cal := c^4 kappa_eff/(8*pi)", "calibrated universal Newton coupling is fair; numeric G_N need not be predicted here", "STRUCTURAL_CALIBRATION_ALLOWED"),
        ("SCI4755_4_Newton", "nabla^2 Phi_N = 4*pi G_cal rho_H", "weak-field Newton law follows if source charge and coupling locks close", "CONDITIONAL_THEOREM_NONCLAIM"),
        ("SCI4755_5_drift", "epsilon_Gsrc includes kappa drift, H_tau integrability, H_ref/tau/frame/boundary/PiH/MHref defects", "unsigned source/coupling clauses remain finite testable residuals", "FINITE_BOUND_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "import_id": import_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for import_id, formula, meaning, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4755_0_accept_clean_private", "Use clean private owner-tail deletion as conditional branch input, not public claim", "SELECTED_PRIVATE_ROUTE"),
        ("ROUTE4755_1_source_coupling", "Move to H_tau/M_Hdress/kappa_eff source-coupling lock", "BEST_NEXT_ROUTE"),
        ("ROUTE4755_2_finite_profile", "If any owner packet clause is unsigned, carry finite owner profile rows", "FALLBACK_ROUTE"),
        ("ROUTE4755_3_public_delay", "Delay public/global local-GR claim until parent selector and source charge/coupling gates close", "PUBLIC_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4755_0_same_branch", "lambda, boundary, incoming, R_Lambda and Kperp clauses close on the same branch", "CONDITIONAL_PRIVATE_ONLY"),
        ("GATE4755_1_parent_selector", "global parent action selector/adoption signed", "OPEN_PUBLIC_PROMOTION_GATE"),
        ("GATE4755_2_source_charge", "H_tau/M_Hdress source charge integrable, positive and same-worldtube", "NEXT_HIGH_LEVERAGE_GATE"),
        ("GATE4755_3_coupling", "kappa_eff/G_cal source-blind with no drift", "OPEN_SOURCE_COUPLING_GATE"),
        ("GATE4755_4_empirical", "arena projection constants and finite bounds source-backed", "OPEN_EMPIRICAL_GATE"),
        ("GATE4755_5_claim", "No local-GR/Newton claim from private owner-tail deletion alone", "FAIL_CLOSED_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, requirement, status in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4755_0_private_not_public", "Do not promote private compact static owner-tail deletion to global/public local GR."),
        ("FW4755_1_same_branch", "Do not combine zero clauses from incompatible branches."),
        ("FW4755_2_Gcal", "Do not pretend calibrated G_cal is a numeric prediction of G_N."),
        ("FW4755_3_no_cancellation", "Do not cancel owner-tail finite residuals against nonowner residuals."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "4755 imports the 4350-4353 clean private RI/Kperp owner packet: the owner channel is conditionally deleted in the private compact static branch, but public/local-GR progress now depends on source charge and calibrated coupling gates.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_PRIVATE_OWNER_PACKET_NONCLAIM",
            "summary": "Owner-tail/Kperp packet conditionally clean on private compact static branch; finite profile fallback retained; source charge/coupling selected next.",
            "claim_status": "NO_LOCAL_GR_OR_NEWTON_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "After deleting the private owner-tail/Kperp channel, the next real local-GR/Newton bottleneck is the source charge and calibrated coupling lock.",
            "preferred_route": "Import and harden H_tau/M_Hdress, kappa_eff=kappa_*Z_H, G_cal and epsilon_Gsrc rows into the current 475x chain.",
            "fallback_route": "If source charge/coupling locks remain unsigned, carry finite transition/source-hair residuals into profile bounds.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], key_field: str, value_field: str) -> str:
    return "\n".join(f"- `{row[key_field]}`: {row[value_field]}" for row in rows)


def write_docs(
    timestamp: str,
    owner_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    coupling_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4755 Y5 R2FR: lambdaRI Boundary Kperp Source Packet Or Profile Demotion

Generated: `{timestamp}`

## Result

4755 imports the later 4350-4353 chain into the current `K_Gamma` rescue. The owner-tail/Kperp channel is conditionally clean in the private compact static branch:

```text
epsilon_owner_tail_Kperp = 0
```

but this is not a public/local-GR claim. The remaining high-leverage bottleneck is now source charge and calibrated coupling: `H_tau/M_Hdress`, `kappa_eff`, `G_cal`, and finite `epsilon_Gsrc` drift/source-hair bounds.

## Owner Packet Resolution

{bullet(owner_rows, "packet_id", "status")}

## Branch Verdict

{bullet(verdict_rows, "verdict_id", "status")}

## Finite Profile Demotion

{bullet(profile_rows, "profile_id", "status")}

## Source Coupling Import

{bullet(coupling_rows, "import_id", "status")}

## Route Matrix

{bullet(routes, "route_id", "status")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 771 PPC4161: lambdaRI Boundary Kperp Source Packet Or Profile Demotion

Generated: `{timestamp}`

## Owner Channel

On the private compact static branch:

```text
lambda_4350 = pi^2/ell_RI^2
B_Lambda = B_RI = I_RI = R_Lambda = 0
Y_Kperp = 0
epsilon_owner_tail_Kperp = 0
```

If any clause is unsigned:

```text
epsilon_owner_tail_Kperp <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350
  + |Pi_a^BRI||B_RI| + |Pi_a^I||I_RI|
  + |W_a^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|).
```

## Source Coupling Next

The next local GR/Newton gate is:

```text
M_H^dress = H_tau - H_ref,
kappa_eff = kappa_* Z_H,
G_cal = c^4 kappa_eff/(8*pi).
```

MTS does not need to predict the numerical value of `G_N` here, but it must lock source charge and remove source/species/frame/range/readout drift.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4755 imports the 4350-4353 RI/Kperp owner-tail cleanup into the current `K_Gamma` chain.
- In the private compact static branch, `epsilon_owner_tail_Kperp=0`.
- If any branch clause is unsigned, the finite profile row is retained instead of hidden.
- The next bottleneck is source charge and calibrated coupling: `M_H^dress=H_tau-H_ref`, `kappa_eff=kappa_*Z_H`, `G_cal=c^4 kappa_eff/(8*pi)`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4755 local packet update: the owner-tail/Kperp channel is conditionally cleaned on the private compact static branch; the next live issue is the Newton source charge and calibrated source coupling lock.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4755-Y5-R2FR-lambdaRI-boundary-Kperp-source-packet-or-profile-demotion.md`

## Decision

`{DECISION}`

## What moved forward

- Imported the 4350-4353 clean RI/Kperp owner-tail chain into the current 475x derivation ladder.
- Marked `epsilon_owner_tail_Kperp=0` on the private compact static branch only.
- Kept finite owner/Kperp profile rows alive if any same-branch clause is unsigned.
- Selected source charge and calibrated coupling as the next local GR/Newton bottleneck.

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
        "4755 imports the clean private RI/Kperp owner-tail packet and selects H_tau/MHref plus calibrated kappa_eff/G_cal as the next Newton/source-coupling gate.",
        "Generated source register, owner packet resolution, branch verdict, finite profile demotion rows, source coupling import, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "private_owner_tail_Kperp_clean_source_coupling_next_nonclaim",
        NEXT_TARGET,
        "Promoting private owner-tail deletion to public local GR, mixing incompatible branch clauses, or treating calibrated G_cal as predicted G_N.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need source charge H_tau/M_Hdress, source-blind kappa_eff/G_cal and finite epsilon_Gsrc drift/hair bounds.",
        "lambdaRI boundary Kperp source packet or profile demotion",
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
    owner_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    coupling_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4755_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4755_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4755_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4755_2_owner_clean", "owner packet includes lambda clean and owner channel deletion", any("lambda_4350" in row["formula"] for row in owner_rows) and any("epsilon_owner_tail_Kperp=0" in row["formula"] for row in owner_rows), str(OWNER_PACKET_CSV)))
    checks.append(("VAL4755_3_branch_verdict", "branch verdict separates private clean and public blocked", any(row["branch"] == "private compact static selector" for row in verdict_rows) and any(row["branch"] == "public/global MTS" and "BLOCKED" in row["status"] for row in verdict_rows), str(BRANCH_VERDICT_CSV)))
    checks.append(("VAL4755_4_profile_fallback", "finite profile demotion retains owner and Kperp bounds", any("Y_owner_a" in row["formula"] for row in profile_rows) and any("Y_Kperp" in row["formula"] for row in profile_rows), str(FINITE_PROFILE_CSV)))
    checks.append(("VAL4755_5_source_coupling", "source coupling import includes M_Hdress, kappa_eff and G_cal", any("M_H^dress" in row["formula"] for row in coupling_rows) and any("kappa_eff" in row["formula"] for row in coupling_rows) and any("G_cal" in row["formula"] for row in coupling_rows), str(SOURCE_COUPLING_IMPORT_CSV)))
    checks.append(("VAL4755_6_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4755_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4755_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4755_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4755_10_claim_row", "claim row L-597 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4755_11_resume", "resume points from 4755 to 4756", "4755-Y5" in resume_text and "4756-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4755_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4755_OVERALL",
            "check": "all 4755 owner-packet/source-coupling nonclaim checks pass",
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
    owner_rows = owner_packet_rows(timestamp)
    verdict_rows = branch_verdict_rows(timestamp)
    profile_rows = finite_profile_rows(timestamp)
    coupling_rows = source_coupling_import_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(OWNER_PACKET_CSV, owner_rows)
    write_csv(BRANCH_VERDICT_CSV, verdict_rows)
    write_csv(FINITE_PROFILE_CSV, profile_rows)
    write_csv(SOURCE_COUPLING_IMPORT_CSV, coupling_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, owner_rows, verdict_rows, profile_rows, coupling_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, owner_rows, verdict_rows, profile_rows, coupling_rows, gates, timestamp))


if __name__ == "__main__":
    main()
