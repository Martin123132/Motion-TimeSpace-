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

CHECKPOINT = "4760"
CLAIM_ID = "L-602"
MARKER = "PPC4161_PARENT_SCALE_LAW_OR_CGAMMA_E00_PROFILE_COEFFICIENT_BOUND_4760"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SCALE_LAW_OR_CGAMMA_E00_PROFILE_COEFFICIENT_BOUND_4760"
DECISION = "PARENT_SCALE_LAW_UNSIGNED_CGAMMA_E00_PROFILE_REDUCED_TO_MEMORY_EXTREMUM_OR_BODY_CHARGE_SCORE_INPUTS_NONCLAIM"
NEXT_TARGET = "4761-Y5-R2FR-same-branch-memory-extremum-signature-or-body-charge-first-fill.md"

DOC_PATH = POST / "4760-Y5-R2FR-parent-scale-law-for-EH-selector-or-cGamma-E00-profile-coefficient-bound.md"
FORMAL_PATH = FORMAL / "776-PPC4161-parent-scale-law-for-EH-selector-or-cGamma-E00-profile-coefficient-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_SOURCE_REGISTER.csv"
SCALE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_PARENT_SCALE_LAW_AUDIT.csv"
CGAMMA_E00_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_CGAMMA_E00_PROFILE_ROWS.csv"
BODY_CHARGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_BODY_CHARGE_INTERFACE_ROLLUP.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_PROMOTION_GATES.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_ROUTE_SELECTION_MATRIX.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4760_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4760_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4760_0_4759_decision", SOURCE_DIR / "P8_Y5_R2FR_4759_DECISION.csv", "AMF_PRIVATE_EH_SELECTOR_EFFECTIVE_BRANCH_RECONCILED_E00_ENVELOPE", "4759 handoff decision"),
    ("SRC4760_1_4759_bound_targets", SOURCE_DIR / "P8_Y5_R2FR_4759_LIVE_BOUND_TARGET_ROWS.csv", "BT4759_0_parent_scale_law", "4759 selected parent scale/E00 fork"),
    ("SRC4760_2_4718_common_G", SOURCE_DIR / "P8_Y5_R2FR_4718_COMMON_G_NORMALIZATION_OWNER_ROWS.csv", "GNL4718_0_Einstein_coupling_law", "common-G normalization law"),
    ("SRC4760_3_4719_linear_bridge", SOURCE_DIR / "P8_Y5_R2FR_4719_LINEARIZED_FIELD_EQUATION_ROWS.csv", "LFE4719_3_Poisson_equation_with_residual", "linearized GR/Poisson residual bridge"),
    ("SRC4760_4_4721_EH_selector", SOURCE_DIR / "P8_Y5_R2FR_4721_TWO_DERIVATIVE_EH_SELECTOR_PROOF_ROWS.csv", "TDEH4721_0_object_language", "two-derivative EH selector proof"),
    ("SRC4760_5_4723_EH_signature", SOURCE_DIR / "P8_Y5_R2FR_4723_EH_SIGNATURE_VERDICT_MATRIX.csv", "VER4723_0_A_MF_variables", "EH selector signature verdict matrix"),
    ("SRC4760_6_4655_cGamma", SOURCE_DIR / "P8_Y5_R2FR_4655_DECISION.csv", "CGAMMA_QUIET_COLLAR_SILENCE_AND_PROFILE_BOUND_INTERFACE_SYNTHESIZED_NONCLAIM", "cGamma quiet collar/profile interface"),
    ("SRC4760_7_4656_memory_extremum", SOURCE_DIR / "P8_Y5_R2FR_4656_DECISION.csv", "PARENT_MEMORY_EXTREMUM_NOHAIR_THEOREM_DERIVED_CURRENT_BRANCH_UNSIGNED", "memory extremum no-hair theorem"),
    ("SRC4760_8_4668_body_charge", SOURCE_DIR / "P8_Y5_R2FR_4668_DECISION.csv", "CMEM_FINAL_ZERO_INSERTED_BODY_CHARGE_REDUCED_TO_BJQ_ZM_SOURCE_CHARGE_GATE", "body-charge reduction after Cmem closure"),
    ("SRC4760_9_4689_score_interface", SOURCE_DIR / "P8_Y5_R2FR_4689_DECISION.csv", "BODY_CHARGE_SCORE_INPUT_INTERFACE_READY_CURRENT_BRANCH_NONCLAIM", "body-charge score interface"),
    ("SRC4760_10_4695_poynting", SOURCE_DIR / "P8_Y5_R2FR_4695_DECISION.csv", "EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT", "Poynting/Hodge once-only gate"),
    ("SRC4760_11_4755_static_packet", SOURCE_DIR / "P8_Y5_R2FR_4755_DECISION.csv", "PRIVATE_STATIC_OWNER_PACKET_CONDITIONALLY_CLEAN", "private static RI/Kperp packet"),
    ("SRC4760_12_4756_newton_bridge", SOURCE_DIR / "P8_Y5_R2FR_4756_DECISION.csv", "STRUCTURAL_NEWTON_BRIDGE_WITH_CALIBRATED_G_DERIVED", "structural Newton bridge with calibrated G"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    SCALE_AUDIT_CSV,
    CGAMMA_E00_CSV,
    BODY_CHARGE_CSV,
    PROMOTION_GATES_CSV,
    ROUTE_MATRIX_CSV,
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


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


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


def scale_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "SCALE4760_0_parent_action",
            "single parent action line for B_GR",
            "S_local[B_GR] candidate exists as an adoption normal form, but not as a parent-derived global action signature.",
            "PARENT_SIGNATURE_UNSIGNED",
            "Find one source action density that signs A_MF, EH selector, no-extra-mode, q-natural descent, common coframe and boundary routing in the same branch.",
        ),
        (
            "SCALE4760_1_A_MF",
            "A_MF / motion-frame axiom",
            "Private branch adopts A_MF as an equivalence-principle-like axiom candidate; older primitives do not derive it globally.",
            "PRIVATE_AXIOM_CANDIDATE",
            "Derive the motion-frame/Cartan object language from MTS primitives or explicitly label it as the local effective branch.",
        ),
        (
            "SCALE4760_2_EH_selector",
            "two-derivative/no-extra-slot EH selector",
            "Exact conditional theorem: if only the observed metric/coframe, compatible connection, volume form and fixed topological data are in the bulk action, EH/Palatini is selected.",
            "EXACT_CONDITIONAL_UNSIGNED",
            "Parent-sign the object-language exhaustion and no-extra-light-mode clauses; covariance alone is not enough.",
        ),
        (
            "SCALE4760_3_scale_gap",
            "IR scale and extra-mode gap",
            "No public proof yet that R2, hidden exchange, fibre/memory and boundary modes are absent/heavy/projected before scoring.",
            "GAP_LAW_MISSING",
            "Either derive a parent Hessian/gap law or retain c_R2/M_R, H_R826 and body-charge finite rows.",
        ),
        (
            "SCALE4760_4_common_G",
            "Newton coupling normalization",
            "The bridge gives G_eff=lambda_D/(8*pi*M_EH^2) after one calibration; it structurally recovers common G but does not predict the numerical value of G_N.",
            "STRUCTURAL_WITH_CALIBRATION",
            "Do not advertise a numerical G derivation; prove common-mode ownership or keep epsilon_Gsrc hair rows.",
        ),
        (
            "SCALE4760_5_static_owner_packet",
            "static RI/Kperp/quarantine owner packet",
            "Private compact static branch conditionally deletes the owner-channel transition residual, but public promotion needs source charge and coupling gates.",
            "PRIVATE_STATIC_CLEAN_NONCLAIM",
            "Use it as a local test collar, not as a global local-GR proof.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "object": obj,
            "finding": finding,
            "status": status,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, obj, finding, status, next_action in specs
    ]


def cgamma_e00_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CG4760_0_E00_master",
            "E_00 profile law",
            "E_00=E_EH_IR+E_nonEH+E_Gamma+E_R826/B826+E_boundary+E_readout",
            "The Poisson bridge is now a coefficient/profile problem, not an undefined local-GR gap.",
            "PROFILE_DECOMPOSED",
        ),
        (
            "CG4760_1_cGamma_product_guard",
            "Gdot product guard",
            "|C_Gamma_Gdot| <= 2.42e-14 yr^-1, C_Gamma_Gdot=J_Gdot^Gamma c_Gamma ||P_Gdot Gamma_mem||+tensor_perp",
            "This bounds a product only; it cannot be divided into c_Gamma without J/profile/tensor-perp units.",
            "SOURCE_BACKED_PRODUCT_NOT_COEFFICIENT",
        ),
        (
            "CG4760_2_memory_extremum_theorem",
            "same-branch memory extremum/no-hair theorem",
            "If matter-scale extremum/no-source bundle, positive memory operator, boundary silence and no extra source slots are parent-signed, then rho_mem=0 -> delta_m=0 -> P Gamma_mem=0 -> E_Gamma=0.",
            "This is the clean derivation-first route for deleting the memory profile without fitting it away.",
            "EXACT_CONDITIONAL_UNSIGNED",
        ),
        (
            "CG4760_3_private_quiet_collar",
            "private quiet-collar branch",
            "A_src, A_lap, boundary and higher-order static memory profile pieces are conditionally silent in the compact ordinary-visible private collar.",
            "This keeps the private local branch internally coherent but does not promote it to a public proof.",
            "PRIVATE_ZERO_CHAIN_NONCLAIM",
        ),
        (
            "CG4760_4_public_finite_profile",
            "public finite cGamma/E00 fallback",
            "|E_Gamma| <= |J_00^Gamma| |c_Gamma| ||P_00 Gamma_mem|| + |tensor_perp|, with the profile norm supplied by body-charge/source-current rows.",
            "This is the scoreable fallback if the memory extremum package stays unsigned.",
            "FIRST_BOUND_FORMULA_READY",
        ),
        (
            "CG4760_5_Poynting_status",
            "EM/Poynting contribution",
            "Poynting is not a free background source: on the same-Hodge/no-wall branch it is counted once as Hilbert EM stress; otherwise it becomes Delta_Hodge_EM, Phi_wall_Poynting or nonminimal coefficient rows.",
            "This answers the Poynting concern without double-counting EM stress.",
            "OWNED_OR_EXPLICIT_BOUND",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "profile_id": profile_id,
            "object": obj,
            "formula_or_contract": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for profile_id, obj, formula, meaning, status in specs
    ]


def body_charge_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "BC4760_0_reduced_source_density",
            "rho_mem",
            "rho_mem=B_mem_eff R_obs + J_mem_live after C_mem^final_live=0 in the strict private branch.",
            "Cmem trace/source-weight block is no longer the live blocker on that branch.",
            "REDUCED_PRIVATE_BRANCH",
        ),
        (
            "BC4760_1_exact_zero_requirements",
            "A_mem=0",
            "Need B_mem_eff=0, J_mem_live=0, Q_boundary_mem=0 and positive Z_mem/M2_mem in the same branch.",
            "This is the real parent-signature target for memory-generated cGamma silence.",
            "SAME_BRANCH_ZERO_PACKAGE_UNSIGNED",
        ),
        (
            "BC4760_2_score_object",
            "I_X^ST",
            "The claim-safe score object is the invariant product of source and test charges over the operator normalization, not raw Z_X or raw Q_X.",
            "Prevents normalization-gauge cheating in R10/PPN/clock/orbital comparisons.",
            "SCORE_INTERFACE_READY",
        ),
        (
            "BC4760_3_source_side",
            "Qbar_XH",
            "Requires positive M_H_ref lower bound, fixed Pi_M, and numerator split Q_bulk+Q_edge+Q_shadow with commutator and denominator drift retained.",
            "Source charge is now concrete but unfilled.",
            "SOURCE_NUMERATOR_OPEN",
        ),
        (
            "BC4760_4_test_side",
            "qbar_XT",
            "Test body response needs matter-marker, EM constant, gauge-kinetic and operator-domain ownership or explicit coefficients.",
            "Keeps WEP/R10/local test scoring nonclaim until test response is sourced.",
            "TEST_RESPONSE_OPEN",
        ),
        (
            "BC4760_5_first_fill",
            "first source-backed row",
            "Best next empirical row is not another generic local-GR statement; it is B_mem/J_mem/Q_boundary/Zmem-M2 or source/test invariant product with units and source path.",
            "Turns the coupling problem into measurable rows.",
            "NEXT_FILL_TARGET",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "rollup_id": rollup_id,
            "object": obj,
            "current_law": law,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for rollup_id, obj, law, meaning, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4760_0_no_public_GR", "Private B_GR/A_MF branch is not public parent-derived MTS-to-GR.", "blocks local-GR overclaim"),
        ("PG4760_1_no_G_prediction", "Common G after one calibration is not a numerical derivation of Newton's constant.", "blocks G_N overclaim"),
        ("PG4760_2_no_product_division", "C_Gamma_Gdot product bounds cannot be divided into c_Gamma without profile/Jacobian/tensor-perp units.", "blocks coefficient shortcut"),
        ("PG4760_3_same_branch", "Zero clauses must be signed in the same branch; do not stitch private zeros from incompatible forks.", "blocks proof collage"),
        ("PG4760_4_Poynting_once", "Poynting is either Hilbert EM stress once or an explicit wall/Hodge/nonminimal coefficient.", "blocks double counting"),
        ("PG4760_5_no_anchor_claim", "Body-charge/R10 rows need numeric units, source paths and valid_for_claim=true before any pass claim.", "keeps empirical interface honest"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "ROUTE4760_0_parent_scale_EH",
            "derive single parent scale/gap/EH selector signature",
            "highest payoff, but 4760 finds it still unsigned; keep as strategic root target.",
            "PRIMARY_LONG_ROUTE_OPEN",
        ),
        (
            "ROUTE4760_1_memory_extremum_signature",
            "parent-sign the memory extremum/no-source/positive-operator package",
            "most direct derivation route for E_Gamma=0 and cGamma profile silence.",
            "SELECTED_NEXT_DERIVATION",
        ),
        (
            "ROUTE4760_2_body_charge_first_fill",
            "fill first source-backed B/J/Q/ZM or invariant product row",
            "best non-circular empirical fallback if extremum signature fails.",
            "SELECTED_FALLBACK",
        ),
        (
            "ROUTE4760_3_R826_R2",
            "attack H_R826/c_R2 scalaron finite rows after memory/source charge",
            "secondary nonEH branch; do not outrank cGamma/source-coupling until memory gate is decided.",
            "DEFERRED_SECONDARY",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4760_0_public_claim", "No R10, WEP, PPN, clock, orbital, Maxwell or local-GR pass from this checkpoint.", "NONCLAIM"),
        ("FW4760_1_G", "Do not say MTS derives the numerical value of G_N; current result is common-G structural recovery after calibration.", "NONCLAIM"),
        ("FW4760_2_cGamma", "Do not turn the Gdot product guard into a cGamma coefficient row without profile/Jacobian data.", "NONCLAIM"),
        ("FW4760_3_branch_stitching", "Do not combine A_MF private adoption, memory extremum and Poynting/Hodge gates unless the same parent branch signs all of them.", "NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4760_0",
            "decision": DECISION,
            "summary": "4760 tries the parent scale-law route and does not close it. The useful advance is sharper: E_Gamma/E00 is reduced to either a same-branch memory extremum theorem or a body-charge/source-test score interface, with Poynting counted once through Hilbert EM stress or explicit wall/Hodge rows.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4760_0",
            "state": "completed_nonclaim",
            "meaning": "The derivation route advanced from generic EH/cGamma language to a precise same-branch memory-extremum versus body-charge fill fork.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The EH scale law is still unsigned, while cGamma/E00 now has a sharp route: parent-sign memory extremum/no-hair or fill the first body-charge/source-test invariant product row.",
            "route_priority": "derive_first_then_fill",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def write_docs(
    timestamp: str,
    scale_rows: list[dict[str, Any]],
    cgamma_rows: list[dict[str, Any]],
    body_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4760: Parent Scale Law for EH Selector or cGamma/E00 Profile Coefficient Bound

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4760 takes the 4759 fork seriously and pushes both sides.

- The parent EH scale-law route is not closed: `A_MF`, the EH selector, common coframe/Hodge, no-extra-mode gap and boundary routing are not yet signed by one parent action branch.
- The useful advance is that the `c_Gamma` / `E_00` branch is no longer vague. It reduces to a precise same-branch memory extremum/no-hair theorem or to explicit body-charge/source-test score inputs.
- The structural Newton bridge is real only after one calibrated `G`: the framework can recover common-G/Poisson form conditionally, but this is not a numerical derivation of Newton's constant.
- Poynting is now placed correctly: either Hilbert-owned EM stress counted once, or explicit wall/Hodge/nonminimal coefficients.
- No public local-GR, R10, WEP, clock, orbital or Maxwell pass is claimed here.

## Parent Scale-Law Audit

{markdown_table(scale_rows, ["audit_id", "object", "status", "next_action"])}

## cGamma / E00 Profile Reduction

{markdown_table(cgamma_rows, ["profile_id", "object", "formula_or_contract", "status"])}

## Body-Charge Interface Rollup

{markdown_table(body_rows, ["rollup_id", "object", "current_law", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4760: EH Scale Law vs cGamma/E00 Profile

Generated: `{timestamp}`

## What Changed

The local-GR bridge is now split into a clean theorem-or-bound fork:

```text
Parent scale law signs B_GR
  => EH principal block + common G after calibration + no extra light modes
  => local GR/Newton/Maxwell private branch can be promoted.
```

That parent scale law is still unsigned.

The live memory branch is now sharper:

```text
If same-branch memory extremum/no-source + positive memory operator
   + boundary silence + no extra source slots,
then rho_mem=0 -> delta_m=0 -> P Gamma_mem=0 -> E_Gamma=0.
```

If that fails, the finite row is:

```text
|E_Gamma| <= |J_00^Gamma| |c_Gamma| ||P_00 Gamma_mem|| + |tensor_perp|.
```

and the profile norm must be supplied by body-charge/source-test invariant product rows, not by hand.

## Coupling Status

`G_eff=lambda_D/(8*pi*M_EH^2)` structurally recovers common `G` after one calibration. It is not yet a numerical prediction of Newton's constant.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4760 finds that the parent EH scale-law route is still unsigned: `A_MF`, no-extra-mode gap, common coframe/Hodge, parent object-language exhaustion and boundary routing are not signed by one global branch.
- It sharpens the surviving `c_Gamma` / `E_00` route into a theorem-or-bound fork: same-branch memory extremum/no-hair gives `E_Gamma=0`, otherwise the body-charge/source-test interface supplies finite profile rows.
- The Newton bridge is structural with calibrated `G_eff=lambda_D/(8*pi*M_EH^2)`, not a numerical derivation of `G_N`.
- Poynting is either counted once as Hilbert EM stress on the same-Hodge branch or becomes explicit wall/Hodge/nonminimal coefficient rows.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4760 packet update: the useful forward route is now the coupling/profile fork. Do not keep circling generic EH language. Try to parent-sign the memory extremum/no-source/positive-operator package; if it fails, fill the first body-charge/source-test invariant product row.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4760-Y5-R2FR-parent-scale-law-for-EH-selector-or-cGamma-E00-profile-coefficient-bound.md`

## Decision

`{DECISION}`

## What moved forward

- The parent EH scale-law route remains open, not falsely closed.
- The `c_Gamma` / `E_00` branch is reduced to a concrete same-branch memory-extremum theorem or finite body-charge/source-test score rows.
- The common-G/Newton bridge is preserved as structural-after-calibration, not a numerical prediction of `G_N`.
- Poynting is placed inside Hilbert EM stress or explicit wall/Hodge/nonminimal coefficient rows.

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
        "local_gr_coupling_profile_fork",
        "4760 reduces the EH/cGamma/E00 route to either a parent-signed memory extremum theorem or explicit body-charge/source-test score inputs.",
        "Generated source register, parent scale audit, cGamma/E00 profile rows, body-charge interface rollup, route matrix, gates, firewalls, decision, status, next target and validation.",
        "parent_scale_law_unsigned_cgamma_E00_profile_reduced_to_memory_extremum_or_body_charge_score_inputs_nonclaim",
        NEXT_TARGET,
        "Mistaking structural common-G calibration for numerical G prediction or product bounds for coefficient bounds.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need same-branch memory extremum signature or first body-charge/source-test invariant product row.",
        "Parent scale law for EH selector or cGamma/E00 profile coefficient bound",
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
    scale_rows: list[dict[str, Any]],
    cgamma_rows: list[dict[str, Any]],
    body_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4760_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4760_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4760_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4760_2_scale_unsigned", "scale audit keeps parent signature and gap law unsigned", any(row["status"] == "PARENT_SIGNATURE_UNSIGNED" for row in scale_rows) and any(row["status"] == "GAP_LAW_MISSING" for row in scale_rows), str(SCALE_AUDIT_CSV)))
    checks.append(("VAL4760_3_common_G_guard", "common G is structural with calibration only", any("does not predict the numerical value" in row["finding"] for row in scale_rows), str(SCALE_AUDIT_CSV)))
    checks.append(("VAL4760_4_cgamma_theorem", "cGamma rows include memory extremum theorem and finite E_Gamma bound", any("rho_mem=0" in row["formula_or_contract"] for row in cgamma_rows) and any("|E_Gamma|" in row["formula_or_contract"] for row in cgamma_rows), str(CGAMMA_E00_CSV)))
    checks.append(("VAL4760_5_body_charge", "body-charge rollup keeps B/J/Q/ZM source-normalization gate open", any("B_mem_eff=0" in row["current_law"] and "Z_mem/M2_mem" in row["current_law"] for row in body_rows), str(BODY_CHARGE_CSV)))
    checks.append(("VAL4760_6_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4760_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4760_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4760_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4760_10_claim_row", "claim row L-602 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4760_11_resume", "resume points from 4760 to 4761", "4760-Y5" in resume_text and "4761-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4760_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(check_passed for _, _, check_passed, _ in checks)
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
            "validation_id": "VAL4760_OVERALL",
            "check": "all 4760 parent-scale/cGamma-E00 profile checks pass",
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
    scale_rows = scale_audit_rows(timestamp)
    cgamma_rows = cgamma_e00_rows(timestamp)
    body_rows = body_charge_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    routes = route_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(SCALE_AUDIT_CSV, scale_rows)
    write_csv(CGAMMA_E00_CSV, cgamma_rows)
    write_csv(BODY_CHARGE_CSV, body_rows)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, scale_rows, cgamma_rows, body_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, scale_rows, cgamma_rows, body_rows, gates, timestamp))


if __name__ == "__main__":
    main()
