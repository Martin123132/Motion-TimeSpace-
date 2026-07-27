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

CHECKPOINT = "4759"
CLAIM_ID = "L-601"
MARKER = "PPC4161_AMF_EH_PRINCIPAL_BLOCK_OR_E00_RESIDUAL_COEFFICIENT_BOUND_4759"
PACKET_MARKER = "PPC4161_PACKET_AMF_EH_PRINCIPAL_BLOCK_OR_E00_RESIDUAL_COEFFICIENT_BOUND_4759"
DECISION = "AMF_PRIVATE_EH_SELECTOR_EFFECTIVE_BRANCH_RECONCILED_E00_ENVELOPE_TO_CGAMMA_R826_BOUND_TARGETS_NONCLAIM"
NEXT_TARGET = "4760-Y5-R2FR-parent-scale-law-for-EH-selector-or-cGamma-E00-profile-coefficient-bound.md"

DOC_PATH = POST / "4759-Y5-R2FR-A-MF-EH-principal-block-or-E00-residual-coefficient-bound.md"
FORMAL_PATH = FORMAL / "775-PPC4161-A-MF-EH-principal-block-or-E00-residual-coefficient-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_SOURCE_REGISTER.csv"
AMF_EH_STATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_AMF_EH_CURRENT_STATE_ROWS.csv"
E00_DECOMP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_E00_RESIDUAL_DECOMPOSITION_ROWS.csv"
NON_EH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_NONEH_ENVELOPE_RECONCILIATION_ROWS.csv"
BOUND_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_LIVE_BOUND_TARGET_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4759_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4759_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4759_0_4758_decision", SOURCE_DIR / "P8_Y5_R2FR_4758_DECISION.csv", "PRIVATE_GR_PARITY_OWNER_EDGE_ACTIVATED", "4758 handoff decision"),
    ("SRC4759_1_4758_survivor", SOURCE_DIR / "P8_Y5_R2FR_4758_LIVE_RESIDUAL_SURVIVOR_ROWS.csv", "LIVE4758_0_A_MF_EH", "4758 A_MF/EH survivor row"),
    ("SRC4759_2_4758_projection", SOURCE_DIR / "P8_Y5_R2FR_4758_EPSILONGSRC_PROJECTION_INPUT_ROWS.csv", "PI4758_2_Poisson_bridge", "4758 Poisson projection row"),
    ("SRC4759_3_4449_decision", SOURCE_DIR / "P8_Y5_R2FR_4449_DECISION.csv", "A_MF_ADOPTED_AS_EXPLICIT_PRIVATE_PARENT_AXIOM_CANDIDATE", "A_MF private adoption decision"),
    ("SRC4759_4_4449_derivation", SOURCE_DIR / "P8_Y5_R2FR_4449_DERIVATION_ROWS.csv", "D4449_1_private_adoption", "A_MF derivation/adoption row"),
    ("SRC4759_5_4720_selector", SOURCE_DIR / "P8_Y5_R2FR_4720_EH_SELECTOR_THEOREM_ROWS.csv", "EHS4720_0_selector_theorem", "EH selector theorem"),
    ("SRC4759_6_4721_selector", SOURCE_DIR / "P8_Y5_R2FR_4721_TWO_DERIVATIVE_EH_SELECTOR_PROOF_ROWS.csv", "TDEH4721_4_verdict", "two-derivative EH selector proof verdict"),
    ("SRC4759_7_4723_verdict", SOURCE_DIR / "P8_Y5_R2FR_4723_EH_SIGNATURE_VERDICT_MATRIX.csv", "VER4723_7_R2_zero_or_source_row", "EH signature verdict matrix"),
    ("SRC4759_8_4538_import", SOURCE_DIR / "P8_Y5_R2FR_4538_GR_PARITY_HQNP_BRANCH_IMPORT.csv", "BI4538_3_Newton_PPN", "private effective local-GR branch import"),
    ("SRC4759_9_4538_residual", SOURCE_DIR / "P8_Y5_R2FR_4538_LOCAL_RESIDUAL_VECTOR_COLLAPSE.csv", "RV4538_5_global_parent_adoption", "private collapse/global blocker"),
    ("SRC4759_10_4539_decision", SOURCE_DIR / "P8_Y5_R2FR_4539_DECISION.csv", "PARENT_ADOPTION_THEOREM_CONDITIONAL", "effective local-GR freeze decision"),
    ("SRC4759_11_4539_contract", SOURCE_DIR / "P8_Y5_R2FR_4539_PARENT_ACTION_SELECTOR_CONTRACT.csv", "PAC4539_4_IR_selector", "parent selector contract"),
    ("SRC4759_12_4540_envelope", SOURCE_DIR / "P8_Y5_R2FR_4540_EFT_RESIDUAL_ENVELOPE.csv", "EFT4540_0_master", "EFT residual envelope"),
    ("SRC4759_13_4541_zeros", SOURCE_DIR / "P8_Y5_R2FR_4541_PRIVATE_ZERO_LAWS.csv", "ZL4541_2_memory_not_inherited", "c_D/deltaK private zeros and cGamma survivor"),
    ("SRC4759_14_4542_bounds", SOURCE_DIR / "P8_Y5_R2FR_4542_STRICTEST_CGAMMA_PRODUCT_BOUNDS.csv", "B4542_CGamma_Gdot", "cGamma product bounds"),
    ("SRC4759_15_4542_requirements", SOURCE_DIR / "P8_Y5_R2FR_4542_PRODUCT_TO_COEFFICIENT_REQUIREMENTS.csv", "CR4542_0_formula", "product-to-coefficient requirements"),
    ("SRC4759_16_4719_poisson", SOURCE_DIR / "P8_Y5_R2FR_4719_LINEARIZED_FIELD_EQUATION_ROWS.csv", "LFE4719_3_Poisson_equation_with_residual", "Poisson residual bridge"),
    ("SRC4759_17_4729_hr826", SOURCE_DIR / "P8_Y5_R2FR_4729_FIRST_HR826_HOM_BOUND_ROW.csv", "HR8264729_0_total", "R826/H_R826 finite Hom-bound row"),
    ("SRC4759_18_4755_decision", SOURCE_DIR / "P8_Y5_R2FR_4755_DECISION.csv", "PRIVATE_STATIC_OWNER_PACKET_CONDITIONALLY_CLEAN", "private RI/Kperp owner packet"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    AMF_EH_STATE_CSV,
    E00_DECOMP_CSV,
    NON_EH_CSV,
    BOUND_TARGET_CSV,
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


def amf_eh_state_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("AMF4759_0_old_derivation_status", "older scalar/flow derivation of A_MF", "not found", "4449 rejects a public derivation from old scalar/flow text alone.", "PUBLIC_AMF_PROOF_NOT_CLAIMED"),
        ("AMF4759_1_private_adoption", "A_MF private parent-branch axiom candidate", "adopted privately", "A_MF gives branch-owned Cartan variables and Noether identities.", "PRIVATE_ADOPTION_ACTIVE"),
        ("AMF4759_2_EH_selector", "two-derivative/no-extra-slot EH selector", "exact conditional theorem", "If parent-signed, EH/Palatini is forced at the principal local order.", "CONDITIONAL_SELECTOR_UNSIGNED"),
        ("AMF4759_3_effective_branch", "PPC4161-GP-HQNP effective local-GR branch", "frozen for private correspondence", "Newton/PPN/source-weight pieces collapse privately on compact ordinary-visible collars.", "EFFECTIVE_LOCAL_GR_BRANCH_ACTIVE_NONCLAIM"),
        ("AMF4759_4_global_parent_gap", "global parent action adoption", "open", "EH/IR selector, sector interfaces, quotient naturality and boundary/no-flux remain parent debts.", "PARENT_THEOREM_NOT_SIGNED"),
        ("AMF4759_5_E00_status", "E_00 Poisson residual", "explicit coefficient target", "Private branch has zero readout; public route needs EH selector or finite E_00 coefficient bounds.", "BOUND_OR_SELECTOR_TARGET"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "state_id": state_id,
            "object": obj,
            "current_result": result,
            "meaning": meaning,
            "status": status,
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for state_id, obj, result, meaning, status in specs
    ]


def e00_decomposition_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("E004759_0_definition", "E_00", "E_00=R_00^local/M_EH^2", "the additive source in nabla^2 Phi_N=4*pi*G_eff*rho+(c^2/2)E_00", "DEFINED_FROM_4719"),
        ("E004759_1_fractional_density", "epsilon_N_density", "epsilon_N <= |E_00|/(kappa_eff rho c^2)+|delta_source|+|Delta_Lambda|/(4*pi*G_eff rho)+|Delta_boundary|/(4*pi*G_eff rho)", "density-region Newton residual contract", "READY_FOR_COEFFICIENTS"),
        ("E004759_2_private_zero", "private GP-HQNP collar", "R_N=0 and R_PPN=0 inside compact ordinary-visible private branch", "useful correspondence branch, not parent theorem", "PRIVATE_EFFECTIVE_ZERO_NONCLAIM"),
        ("E004759_3_selector_piece", "E_EH_IR", "zero if parent scale/gap law signs EH/Palatini IR selector", "turns effective EH into MTS-owned local principal block", "PRIMARY_DERIVATION_TARGET"),
        ("E004759_4_nonEH_piece", "E_nonEH", "sum_i J_00^i c_i", "explicit EFT residual envelope for extra invariant terms", "BOUND_ENVELOPE_ACTIVE"),
        ("E004759_5_memory_piece", "E_Gamma", "J_00^Gamma c_Gamma ||P_00 Gamma_mem|| + tensor_perp", "MTS-specific memory/channel residue; product bounds exist but coefficient map missing", "CGAMMA_PROFILE_TARGET"),
        ("E004759_6_hidden_R826_piece", "E_R826/B826", "controlled by H_R826_total and root/coercivity rows if R826 object-language exhaustion is unsigned", "hidden exchange branch feeds curvature-square/nonEH residuals", "HR826_BOUND_TARGET"),
        ("E004759_7_boundary_readout_piece", "E_boundary+E_readout", "boundary/source charge/readout/projector tails", "must be zero by parent collar/no-flux or retained as finite source rows", "RETAINED_GUARD"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "component": component,
            "formula": formula,
            "meaning": meaning,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, component, formula, meaning, status in specs
    ]


def non_eh_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("NEH4759_0_master", "E_IR_local(A)", "|R_A| <= |J_A^D c_D|+|J_A^k delta_kappa|+|J_A^G c_Gamma|+|J_A^T c_T|+|J_A^R c_R2/M_R^2|+|J_A^B c_bdy|", "active envelope unless parent scale/gap law closes extra invariants", "ACTIVE_NONCLAIM_ENVELOPE"),
        ("NEH4759_1_cD", "c_D", "0 inside PPC4161-GP-HQNP effective local branch", "same-coframe/disformal failure privately closed", "PRIVATE_ZERO"),
        ("NEH4759_2_deltaKappa", "delta_kappa", "0 inside PPC4161-GP-HQNP effective local branch", "relative source/coupling drift privately closed; numeric G still calibrated", "PRIVATE_ZERO"),
        ("NEH4759_3_cGamma", "c_Gamma", "|C_Gamma_Gdot| <= 2.42e-14 yr^-1 as product bound", "primary MTS-specific memory residual; need J_Gdot^Gamma and profile norm", "PRIMARY_BOUND_TARGET"),
        ("NEH4759_4_cR2_R826", "c_R2/M_R^2 and R826 hidden exchange", "c_R2_eff includes visible, bare, hidden exchange, measure and boundary pieces; H_R826_total components missing", "R2/scalaron finite branch reduced to object-language/source-bound targets", "SECONDARY_BOUND_TARGET"),
        ("NEH4759_5_cT_cBdy", "c_T/c_bdy", "torsion/nonmetricity and boundary charge terms retained unless algebraic/heavy/topological/routed", "preferred-frame, source-normalization and clock/orbital tails", "RETAINED_BOUND_TARGETS"),
        ("NEH4759_6_KGamma_packet", "KGamma RI/Kperp owner packet", "conditionally clean in private compact static branch", "helps static local branch but does not globalize parent EH/scale law", "PRIVATE_STATIC_OWNER_PACKET"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "coefficient_or_family": family,
            "current_formula_or_bound": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, family, formula, meaning, status in specs
    ]


def bound_target_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("BT4759_0_parent_scale_law", "derive parent scale/gap law for EH selector", "A_MF + scale hierarchy + no extra light modes + same coframe", "would promote EH principal block from effective to parent-owned", "DERIVATION_FIRST"),
        ("BT4759_1_E00_coefficient", "first E_00 coefficient bound", "|E_00|/(kappa_eff rho c^2) below Newton/Poisson tolerance", "makes 4719 Poisson bridge scoreable outside private branch", "COEFFICIENT_ROW_NEEDED"),
        ("BT4759_2_cGamma_Gdot", "c_Gamma product-to-profile coefficient", "C_Gamma_Gdot = J_Gdot^Gamma c_Gamma ||P_Gdot Gamma_mem|| + tensor_perp; bound <=2.42e-14 yr^-1", "first source-backed product guard; not c_Gamma alone", "PRIMARY_EMPIRICAL_FALLBACK"),
        ("BT4759_3_HR826_total", "H_R826_total bound", "H_hidden+H_readout+H_domain+H_source_shadow+H_block+H_extra_mass+H_rad", "finite hidden-exchange/root branch if object-language exhaustion stays unsigned", "SECONDARY_EMPIRICAL_FALLBACK"),
        ("BT4759_4_R2_alpha_lambda", "R2/f(R) scalaron row", "alpha_R(lambda_R) against full alpha_bound(lambda), plus gamma/beta projections", "range/scalar fallback if EH two-derivative selector remains unsigned", "R10_CURVE_REQUIRED"),
        ("BT4759_5_boundary_sector", "boundary/no-flux collar proof or bound", "E_boundary routed as Hamiltonian/topological charge or finite exterior source row", "needed for public inverse-square/alpha3/clock claims", "RETAINED_GUARD"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "target_id": target_id,
            "target": target,
            "required_law_or_input": law,
            "why_it_matters": why,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for target_id, target, law, why, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4759_0_parent_scale_EH", "derive parent scale/gap law for the EH selector", "best theory route; upgrades effective local GR toward parent-derived MTS local GR", "SELECTED_PRIMARY"),
        ("ROUTE4759_1_cGamma_E00_profile", "convert C_Gamma_Gdot product bound into c_Gamma/profile coefficient row", "best immediate bound route because a source-backed product bound exists", "SELECTED_PARALLEL"),
        ("ROUTE4759_2_HR826_hidden", "fill or zero first H_R826 component", "attacks hidden exchange/root branch after cGamma", "SECONDARY"),
        ("ROUTE4759_3_R2_curve", "run R2 alpha(lambda) only after parent coefficients or full curve exist", "prevents anchor-only fifth-force overclaim", "DEFERRED"),
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


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4759_0_private_branch", "private effective local-GR branch is not public parent-derived local GR", "blocks effective-branch overclaim"),
        ("PG4759_1_A_MF", "A_MF private adoption is not older-primitives derivation", "keeps parent signature burden explicit"),
        ("PG4759_2_EH_selector", "two-derivative EH selector must be parent-signed, not inferred from covariance alone", "blocks covariance-only proof"),
        ("PG4759_3_E00", "Poisson E_00 residual must be zero or bounded before Newton/local-GR claim", "keeps coefficient targets live"),
        ("PG4759_4_product_bound", "C_Gamma_Gdot product bound cannot be divided into c_Gamma without J/profile units", "blocks product-to-coefficient shortcut"),
        ("PG4759_5_no_cancellation", "do not cancel non-EH, boundary, memory or source tails against calibrated G or fitted ephemeris", "keeps residual envelope no-cancellation"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4759_0_do_not_rewind", "Do not keep treating A_MF as untouched: it is privately adopted as an axiom candidate."),
        ("FW4759_1_do_not_overclaim", "Do not call the private GP-HQNP effective branch a public parent-derived MTS->GR proof."),
        ("FW4759_2_metric_side_now", "Source-weight coupling is no longer the main private-branch blocker; the live root is metric principal-block ownership and residual coefficients."),
        ("FW4759_3_bound_or_derive", "Every E_00/non-EH component must be derived zero or carried as a finite source-backed bound row."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
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
            "meaning": "4759 reconciles the metric-side corpus: A_MF is privately adopted, the EH selector is an exact conditional theorem, and the GP-HQNP branch is a disciplined effective local-GR branch; public parent-derived local GR still needs a parent scale/EH selector or finite E00/nonEH coefficient bounds, with cGamma and H_R826 as the first concrete bound targets.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STAT4759_0",
            "summary": "Metric principal-block state reconciled: private effective local GR retained, parent theorem not claimed, E00/nonEH bound queue selected.",
            "claim_status": "PRIVATE_EFFECTIVE_BRANCH_PLUS_PUBLIC_RESIDUAL_QUEUE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "recommended_first_move": "Try the parent scale/gap law for the EH selector; in parallel, turn C_Gamma_Gdot into a profile-coefficient E00 row with explicit J_Gdot^Gamma, units and no-cancellation guard.",
            "why": "This is the cleanest next fork: either own the metric principal block, or make the first surviving memory/E00 residual coefficient genuinely scoreable.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, divider, *body])


def write_docs(
    timestamp: str,
    amf_rows: list[dict[str, Any]],
    e00_rows: list[dict[str, Any]],
    non_eh: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4759: A_MF / EH Principal Block or E00 Residual Coefficient Bound

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4759 reconciles the metric-side route with the current corpus.

- `A_MF` is not untouched: it is privately adopted as a PPC4161 parent-branch axiom candidate.
- The two-derivative/no-extra-slot EH selector is an exact conditional theorem, but not globally parent-signed.
- The `PPC4161-GP-HQNP` branch is a disciplined effective local-GR branch for private correspondence, not a public MTS-to-GR proof.
- The public/theory frontier is now `A_MF`/EH scale ownership or finite `E_00`/non-EH coefficient bounds.
- The first concrete bound route is `c_Gamma` through the source-backed product guard `|C_Gamma_Gdot| <= 2.42e-14 yr^-1`; it still needs profile/Jacobian units before becoming a `c_Gamma` bound.

## A_MF / EH Current State

{markdown_table(amf_rows, ["state_id", "object", "current_result", "status"])}

## E00 Residual Decomposition

{markdown_table(e00_rows, ["component_id", "component", "formula", "current_status"])}

## nonEH Envelope Reconciliation

{markdown_table(non_eh, ["row_id", "coefficient_or_family", "current_formula_or_bound", "status"])}

## Live Bound Targets

{markdown_table(bounds, ["target_id", "target", "required_law_or_input", "selection_status"])}

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

    formal = f"""# PPC4161 4759: A_MF / EH / E00 Reconciliation

Generated: `{timestamp}`

## Current Metric-Side State

The local metric route is no longer an empty gap:

```text
A_MF = adopted private parent-branch axiom candidate
EH selector = exact conditional two-derivative/no-extra-slot theorem
PPC4161-GP-HQNP = effective private local-GR branch
```

The public theorem is still not proved because the parent action has not signed the EH/IR scale law and all global sector-interface clauses.

## Poisson Residual Target

From the 4719 bridge,

```text
nabla^2 Phi_N = 4*pi*G_eff*rho + (c^2/2)E_00
E_00 = R_00^local/M_EH^2
```

with the density-region gate

```text
epsilon_N <= |E_00|/(kappa_eff rho c^2)
           + |delta_source|
           + |Delta_Lambda|/(4*pi*G_eff rho)
           + |Delta_boundary|/(4*pi*G_eff rho).
```

Current decomposition:

```text
E_00 = E_EH_IR + E_nonEH + E_Gamma + E_R826/B826
     + E_boundary + E_readout.
```

Inside the private `PPC4161-GP-HQNP` branch, the local Newton/PPN readout is closed by construction. Outside that branch, every term must be parent-zero or source-backed.

## First Surviving Bound Target

The active memory/product guard is

```text
|C_Gamma_Gdot| <= 2.42e-14 yr^-1
C_Gamma_Gdot = J_Gdot^Gamma c_Gamma ||P_Gdot Gamma_mem|| + tensor_perp.
```

This is not yet a `c_Gamma` value. It becomes scoreable only after `J_Gdot^Gamma`, the memory-profile norm, tensor-perp term, units and no-cancellation guard are fixed.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4759 reconciles the metric-side local-GR branch with current evidence: `A_MF` is privately adopted, the EH selector is exact conditional, and `PPC4161-GP-HQNP` is a disciplined effective local-GR branch.
- This is not a public parent-derived MTS-to-GR theorem. The parent scale/EH selector and global sector-interface clauses remain unsigned.
- The `E_00` Poisson residual is now decomposed into `E_EH_IR`, `E_nonEH`, `E_Gamma`, `E_R826/B826`, boundary and readout pieces.
- First concrete bound route: `|C_Gamma_Gdot| <= 2.42e-14 yr^-1`, pending `J_Gdot^Gamma`, profile norm, tensor-perp term and units.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4759 local packet update: stop circling generic EH language. The private effective local-GR branch exists; the public proof route is parent scale/EH selector, and the finite route starts with `E_00`/`c_Gamma` product-to-profile coefficient rows.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4759-Y5-R2FR-A-MF-EH-principal-block-or-E00-residual-coefficient-bound.md`

## Decision

`{DECISION}`

## What moved forward

- Reconciled the metric-side state: `A_MF` is privately adopted, EH is conditionally selected, and `PPC4161-GP-HQNP` is a frozen effective local-GR branch.
- Kept public/parent-derived local GR unclaimed because the parent scale/EH selector and global sector interfaces remain unsigned.
- Decomposed `E_00` into EH/IR, nonEH, memory, R826/B826, boundary and readout components.
- Selected the next real fork: parent scale/gap law for EH, or convert `C_Gamma_Gdot` into a source-backed `E_00`/`c_Gamma` coefficient row.

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
        "local_gr_metric_principal_block_reconciliation",
        "4759 reconciles A_MF, EH selector, private effective local-GR branch, and E00/nonEH coefficient-bound queue.",
        "Generated source register, A_MF/EH state rows, E00 decomposition rows, nonEH envelope reconciliation, live bound targets, route matrix, gates, firewalls, decision, status, next target and validation.",
        "AMF_private_EH_selector_E00_cGamma_R826_bound_targets_nonclaim",
        NEXT_TARGET,
        "Calling the private effective branch a public parent-derived local-GR proof or converting product bounds into coefficients without profile units.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need parent scale/EH selector or source-backed E00/cGamma profile coefficient bound.",
        "A_MF EH principal block or E00 residual coefficient bound",
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
    amf_rows: list[dict[str, Any]],
    e00_rows: list[dict[str, Any]],
    non_eh: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4759_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4759_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4759_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4759_2_amf_state", "A_MF private adoption and public parent gap are both present", any(row["status"] == "PRIVATE_ADOPTION_ACTIVE" for row in amf_rows) and any(row["status"] == "PARENT_THEOREM_NOT_SIGNED" for row in amf_rows), str(AMF_EH_STATE_CSV)))
    checks.append(("VAL4759_3_e00_decomp", "E00 decomposition includes density gate and cGamma/R826 components", any(row["component"] == "epsilon_N_density" and "E_00" in row["formula"] for row in e00_rows) and any("E_Gamma" in row["component"] for row in e00_rows) and any("E_R826" in row["component"] for row in e00_rows), str(E00_DECOMP_CSV)))
    checks.append(("VAL4759_4_noneh", "nonEH envelope keeps c_D/deltaK private zeros and cGamma primary target", any(row["coefficient_or_family"] == "c_D" and row["status"] == "PRIVATE_ZERO" for row in non_eh) and any(row["coefficient_or_family"] == "delta_kappa" and row["status"] == "PRIVATE_ZERO" for row in non_eh) and any(row["coefficient_or_family"] == "c_Gamma" and "2.42e-14" in row["current_formula_or_bound"] for row in non_eh), str(NON_EH_CSV)))
    checks.append(("VAL4759_5_bounds", "live bounds include parent scale law, cGamma product and H_R826", any("scale/gap" in row["target"] for row in bounds) and any("2.42e-14" in row["required_law_or_input"] for row in bounds) and any("H_R826_total" in row["target"] for row in bounds), str(BOUND_TARGET_CSV)))
    checks.append(("VAL4759_6_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4759_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4759_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4759_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4759_10_claim_row", "claim row L-601 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4759_11_resume", "resume points from 4759 to 4760", "4759-Y5" in resume_text and "4760-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4759_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4759_OVERALL",
            "check": "all 4759 AMF/EH/E00 reconciliation checks pass",
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
    amf_rows = amf_eh_state_rows(timestamp)
    e00_rows = e00_decomposition_rows(timestamp)
    non_eh = non_eh_rows(timestamp)
    bounds = bound_target_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(AMF_EH_STATE_CSV, amf_rows)
    write_csv(E00_DECOMP_CSV, e00_rows)
    write_csv(NON_EH_CSV, non_eh)
    write_csv(BOUND_TARGET_CSV, bounds)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, amf_rows, e00_rows, non_eh, bounds, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, amf_rows, e00_rows, non_eh, bounds, gates, timestamp))


if __name__ == "__main__":
    main()
