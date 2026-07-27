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

CHECKPOINT = "4758"
CLAIM_ID = "L-600"
MARKER = "PPC4161_OWNER_NOWA_EDGE_ACTIVATION_OR_EPSILONGSRC_PROJECTION_INPUTS_4758"
PACKET_MARKER = "PPC4161_PACKET_OWNER_NOWA_EDGE_ACTIVATION_OR_EPSILONGSRC_PROJECTION_INPUTS_4758"
DECISION = "PRIVATE_GR_PARITY_OWNER_EDGE_ACTIVATED_FOR_SOURCE_WEIGHTS_POISSON_EPSILONGSRC_PROJECTION_ROWS_RECONCILED_NONCLAIM"
NEXT_TARGET = "4759-Y5-R2FR-A-MF-EH-principal-block-or-E00-residual-coefficient-bound.md"

DOC_PATH = POST / "4758-Y5-R2FR-owner-no-wA-edge-activation-or-epsilonGsrc-projection-inputs.md"
FORMAL_PATH = FORMAL / "774-PPC4161-owner-no-wA-edge-activation-or-epsilonGsrc-projection-inputs.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_SOURCE_REGISTER.csv"
OWNER_EDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_OWNER_EDGE_ACTIVATION_ROWS.csv"
SOURCE_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_PRIVATE_SOURCE_ZERO_PROPAGATION_ROWS.csv"
PROJECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_EPSILONGSRC_PROJECTION_INPUT_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_LIVE_RESIDUAL_SURVIVOR_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4758_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4758_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4758_0_4757_decision", SOURCE_DIR / "P8_Y5_R2FR_4757_DECISION.csv", "COMMON_MODE_GRAMMAR_CONDITIONAL_OWNER_NO_WA_UNSIGNED_EPSILONGSRC_FINITE_INPUT_RUNNER_STAGED_NONCLAIM", "4757 fork"),
    ("SRC4758_1_4757_next", SOURCE_DIR / "P8_Y5_R2FR_4757_NEXT_TARGET.csv", "owner/no-wA edge package", "4758 target handoff"),
    ("SRC4758_2_4446_decision", SOURCE_DIR / "P8_Y5_R2FR_4446_DECISION.csv", "GR_PARITY_STANDARD_MATTER_IMPORT_PRIVATE_BRANCH_ADOPTED", "private GR-parity adoption decision"),
    ("SRC4758_3_4446_adoption", SOURCE_DIR / "P8_Y5_R2FR_4446_GR_PARITY_ADOPTION_OUTPUT.csv", "ADOPT4446_0_PPC4161_GR_parity_import", "private adoption row"),
    ("SRC4758_4_4446_residual", SOURCE_DIR / "P8_Y5_R2FR_4446_SOURCE_UNIVERSALITY_RESIDUAL_VECTOR.csv", "RU4446_0_Delta_w_A", "source universality residual vector"),
    ("SRC4758_5_4447_decision", SOURCE_DIR / "P8_Y5_R2FR_4447_DECISION.csv", "SOURCE_UNIVERSALITY_PIECES_PROPAGATED", "source pieces propagated to residual vector"),
    ("SRC4758_6_4447_ppn", SOURCE_DIR / "P8_Y5_R2FR_4447_PPN_SOURCE_RESIDUAL_OUTPUT.csv", "PPN4447_1_gamma_minus_1_source_norm", "PPN source subvector zero"),
    ("SRC4758_7_4447_rollup", SOURCE_DIR / "P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv", "RU4447_0_source_weight_subvector", "source-weight rollup"),
    ("SRC4758_8_4448_survivors", SOURCE_DIR / "P8_Y5_R2FR_4448_SURVIVOR_MAP_OUTPUT.csv", "SURV4448_0_A_MF_parent_motion_frame", "live survivor map"),
    ("SRC4758_9_4717_contract", SOURCE_DIR / "P8_Y5_R2FR_4717_PARENT_SIGNATURE_CONTRACT.csv", "PSC4717_0_single_density_line", "no-preaction source prefactor contract"),
    ("SRC4758_10_4718_action", SOURCE_DIR / "P8_Y5_R2FR_4718_PARENT_ACTION_SIGNATURE_ROWS.csv", "PAS4718_0_candidate_parent_action", "parent action signature"),
    ("SRC4758_11_4718_G", SOURCE_DIR / "P8_Y5_R2FR_4718_COMMON_G_NORMALIZATION_OWNER_ROWS.csv", "GNL4718_0_Einstein_coupling_law", "common G owner law"),
    ("SRC4758_12_4719_linear", SOURCE_DIR / "P8_Y5_R2FR_4719_LINEARIZED_FIELD_EQUATION_ROWS.csv", "LFE4719_3_Poisson_equation_with_residual", "linearized Poisson bridge"),
    ("SRC4758_13_4719_bound", SOURCE_DIR / "P8_Y5_R2FR_4719_POISSON_RESIDUAL_BOUND_ROWS.csv", "PB4719_1_fractional_density_region", "Poisson residual bound"),
    ("SRC4758_14_4719_ppn", SOURCE_DIR / "P8_Y5_R2FR_4719_PPN_RESIDUAL_VECTOR_ROWS.csv", "PPNV4719_0_gamma", "PPN residual vector"),
    ("SRC4758_15_4370_KN", SOURCE_DIR / "P8_Y5_R2FR_4370_BOUND_THEOREMS.csv", "TH4370_3_safe_bound_selector", "zero-monopole Newton geometry gate"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    OWNER_EDGE_CSV,
    SOURCE_ZERO_CSV,
    PROJECTION_CSV,
    SURVIVOR_CSV,
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


def owner_edge_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("OE4758_0_private_SM_import", "one imported S_matter scalar density functor with no SpeciesLabel/MaterialLabel -> Coeff_active_source morphism", "Delta_w_A and material active-source reentry", "PRIVATE_BRANCH_ACTIVATED_BY_4446", "public/strict primitive derivation still false"),
        ("OE4758_1_single_density_line", "one common lambda_D matter action-density line", "relative w_A/action-scale drift", "CANDIDATE_PARENT_SIGNATURE_FROM_4717_4718", "parent coefficients lambda_D and M_EH^2 not primitive-derived"),
        ("OE4758_2_variation_before_readout", "vary once before source/test readout and calibration maps", "post-variation current/source rescale as parent coupling", "SUPPORTED_BY_4716_4718_SIGNATURE", "global parent signature still nonclaim"),
        ("OE4758_3_common_G_owner", "G_eff=lambda_D/(8*pi*M_EH^2)", "universal normalization separated from relative source prefactors", "DERIVED_CONDITIONALLY_FROM_ACTION_SIGNATURE", "numeric G_N remains calibrated unless lambda_D and M_EH^2 are derived"),
        ("OE4758_4_public_zero_control", "same branch demanded as public/strict MTS primitive theorem", "public Delta_w_A=0 claim", "NOT_ACTIVATED", "strict primitive SM/no-source-prefactor origin remains open"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "edge_id": edge_id,
            "edge_or_signature": edge,
            "kills_or_controls": kills,
            "activation_status": status,
            "remaining_guard": guard,
            "private_branch_zero_allowed": status.startswith("PRIVATE_BRANCH_ACTIVATED"),
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for edge_id, edge, kills, status, guard in specs
    ]


def source_zero_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SZ4758_0_Delta_w_A", "relative component source weight", "0", "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH", "RU4446_0_Delta_w_A", "material/R_eq empirical fallback if private adoption is rejected"),
        ("SZ4758_1_material_reentry", "material label to active-source coefficient reentry", "0", "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH", "RU4446_1_material_readout_reentry", "source-backed material projection tensor still needed for empirical inventory"),
        ("SZ4758_2_WEP_eta_source_piece", "WEP eta source-weight contribution", "0", "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH", "PPN4447_0_WEP_eta_source_charge", "source-universality subvector only; full WEP/material values not claimed"),
        ("SZ4758_3_gamma_beta_source_norm", "PPN gamma/beta source-normalization pieces", "0", "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH", "PPN4447_1_gamma_minus_1_source_norm; PPN4447_2_beta_minus_1_source_norm", "EH principal block, scalar/disformal and nonlinear metric readout remain"),
        ("SZ4758_4_preferred_frame_source_piece", "alpha_i/xi/zeta source-weight pieces", "0", "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH", "PPN4447_3 through PPN4447_5", "domain/projector, boundary and conservation side channels remain"),
        ("SZ4758_5_Gdot_clock_orbital_source_piece", "Gdot/clock/orbital material-reentry source pieces", "0", "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH", "PPN4447_6 through PPN4447_8", "common G stationarity, clock/EM/Hodge and orbital source-charge glue remain"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": zero_id,
            "subvector": subvector,
            "private_branch_value": value,
            "status": status,
            "source_anchor": anchor,
            "survivor": survivor,
            "full_observable_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for zero_id, subvector, value, status, anchor, survivor in specs
    ]


def projection_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PI4758_0_common_G_owner", "common-G/Newton coupling", "G_eff=lambda_D/(8*pi*M_EH^2)", "lambda_D, M_EH^2", "universal scale separated from source-prefactor residuals", "NUMERIC_G_NOT_DERIVED"),
        ("PI4758_1_parent_field_equation", "local field equation", "G_mu_nu=kappa_eff T_mu_nu+E_mu_nu", "kappa_eff=lambda_D/M_EH^2; E_mu_nu=R_mu_nu^local/M_EH^2", "explicit GR residual container", "CONDITIONAL_EH_SIGNATURE"),
        ("PI4758_2_Poisson_bridge", "Newton/Poisson source", "nabla^2 Phi_N=4*pi*G_eff*rho+(c^2/2)E_00", "E_00; rho; same Hilbert source charge", "turns local Newton bridge into a coefficient test", "DERIVED_CONDITIONALLY"),
        ("PI4758_3_density_residual", "fractional density-region Newton residual", "epsilon_N <= |E_00|/(kappa_eff rho c^2) + |delta_source| + |Delta_Lambda|/(4*pi*G_eff rho) + |Delta_boundary|/(4*pi*G_eff rho)", "E_00, delta_source, Delta_Lambda, Delta_boundary", "first direct epsilon_Gsrc projection formula against local Newton source density", "READY_FOR_NUMERIC_COEFFICIENTS"),
        ("PI4758_4_exterior_force", "exterior inverse-square residual", "|Delta a_r|/|G_eff M_H/r^2| <= |int E_00 dV|/(kappa_eff M_H c^2) + |delta_M_H|/M_H + |multipoles|/(M_H r^l) + |boundary_flux|/(G_eff M_H)", "E_00 integral, M_H, multipoles, boundary flux", "separates source charge from orbital GM readout", "READY_FOR_ORBITAL_GATE"),
        ("PI4758_5_zero_monopole_perp", "epsilon_Gsrc_perp compact-source gate", "E_perp <= delta_N/K_N(s); K_N(s)=min((1-s)^-2, 2s(1-s)^-3)", "delta_N, s=R/r, E_perp components", "retains the sharper 4370 source-shape suppression gate", "GEOMETRY_READY_COEFFICIENTS_MISSING"),
        ("PI4758_6_PPN_vector", "PPN residual vector", "gamma,beta,alpha_i,xi,zeta_i,Gdot = Pi_PPN[E_mu_nu, domain/projector, scalar/disformal, boundary, EM/Poynting, common-G drift]", "shared PPN convention and transfer matrices", "Poisson does not by itself prove local GR", "PPN_VECTOR_STAGED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "projection_id": projection_id,
            "arena": arena,
            "projection_formula": formula,
            "required_inputs": inputs,
            "what_it_buys": buys,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for projection_id, arena, formula, inputs, buys, status in specs
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("LIVE4758_0_A_MF_EH", "A_MF parent motion-frame / EH principal block", "gamma,beta,Newtonian metric principal block", "PRIMARY_DERIVATION_TARGET", "derive or explicitly adopt A_MF and parent-sign EH normal form"),
        ("LIVE4758_1_E00_local_residual", "E_00 = R_00^local/M_EH^2", "Poisson/Newton density and exterior force residual", "FIRST_COEFFICIENT_BOUND_TARGET", "derive zero or source bound for E_00"),
        ("LIVE4758_2_PPN_non_source", "non-source PPN vector", "gamma,beta,alpha_i,xi,zeta_i,Gdot", "SURVIVES_AFTER_SOURCE_WEIGHT_ZERO", "same-metric EH readout, no scalar/disformal bulk, no domain/projector drift, boundary silence"),
        ("LIVE4758_3_material_Req", "material/R_eq empirical values", "WEP, clock, orbital compact-test rows", "EMPIRICAL_FALLBACK", "fill projection coefficient, residual value, bound and source path"),
        ("LIVE4758_4_R10_curve", "R10 alpha(lambda) curve / fifth-force envelope", "short-range range hair", "SECONDARY_EMPIRICAL_FALLBACK", "full bound curve and mapped MTS parent coefficients"),
        ("LIVE4758_5_EM_Poynting", "EM/Poynting Hilbert owner", "zeta3, preferred-frame, WEP/clock EM leak", "CLOSED_PRIVATE_WITH_GUARD", "retain deformation/radiative boundary tails only"),
        ("LIVE4758_6_common_G_stationarity", "D_tau ln(lambda_D/M_EH^2)", "Gdot/G, orbital, clock drift", "OPEN_COMMON_SCALE_DRIFT_GATE", "derive constants/superselection labels or cancellation identity"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "observable_targets": targets,
            "current_status": status,
            "next_action": action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, targets, status, action in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4758_0_A_MF_EH", "derive/adopt parent motion-frame gauge A_MF and EH principal block", "upgrades Poisson/PPN from effective GR infrastructure toward MTS-owned local GR", "SELECTED_NEXT"),
        ("ROUTE4758_1_E00_bound", "derive zero or finite coefficient bound for E_00", "makes the 4719 Poisson residual scoreable", "PARALLEL_SELECTED"),
        ("ROUTE4758_2_material_Req", "fill first material/R_eq empirical value", "empirical fallback if EH/A_MF derivation stalls", "FALLBACK"),
        ("ROUTE4758_3_R10_curve", "source full alpha(lambda) curve and MTS coefficients", "range-hair test once parent coefficients exist", "LATER"),
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
        ("PG4758_0_private_not_public", "private source-weight zero does not equal public/strict primitive proof", "blocks overclaiming 4446 adoption"),
        ("PG4758_1_source_zero_not_full_PPN", "Delta_w_A=0 source subvector does not close gamma/beta/alpha_i/xi/zeta/Gdot", "keeps PPN vector live"),
        ("PG4758_2_poisson_not_full_GR", "Poisson recovery does not prove full local GR", "keeps spatial/nonlinear/vector/conservation gates live"),
        ("PG4758_3_numeric_G_firewall", "G_eff owner law does not predict measured G_N unless lambda_D and M_EH^2 are derived", "keeps common calibration honest"),
        ("PG4758_4_no_R10_WEP_claim", "WEP/R10 anchors remain fallback evidence, not claims from source-universality", "keeps empirical tests disciplined"),
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
        ("FW4758_0_no_regression", "Do not regress from 4446/4447: Delta_w_A is zero inside the private GR-parity import branch."),
        ("FW4758_1_no_public_overclaim", "Do not present private branch adoption as a public primitive derivation from motion/time/space."),
        ("FW4758_2_no_poisson_only_GR", "Do not call local GR closed from Poisson alone; PPN and conservation rows stay explicit."),
        ("FW4758_3_no_hidden_coupling", "Do not hide E_00, boundary, scalar/disformal, projector, EM/Poynting or Gdot tails inside calibrated G."),
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
            "meaning": "4758 reconciles the older owner/no-wA fork with newer corpus evidence: source-weight/material-reentry residuals are zero inside the private GR-parity standard-matter import branch, while public primitive derivation, EH/A_MF ownership, E00/PPN residuals, common-G stationarity and empirical material/R10 values remain open.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STAT4758_0",
            "summary": "Owner/no-wA source-weight leg activated privately; epsilon_Gsrc projection rows rebased onto 4718/4719 common-G and Poisson residual equations.",
            "claim_status": "PRIVATE_BRANCH_PROGRESS_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "recommended_first_move": "Attack A_MF/EH principal-block ownership and the E_00 residual coefficient together: prove the local metric block is parent-owned or produce the first source-backed E_00 bound row.",
            "why": "The main source-weight coupling gremlin is privately closed, so the honest local-GR bottleneck shifts to metric principal-block ownership and explicit residual coefficients.",
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
    owner_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4758: Owner/no-wA Edge Activation or epsilon_Gsrc Projection Inputs

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4758 corrects the live state rather than repeating the older 4361/4370 blockage.

- The owner/no-`w_A` source-weight leg **is activated inside the private PPC4161 GR-parity standard-matter import branch**.
- This makes `Delta_w_A=0` and material active-source reentry `=0` in that private branch.
- This is still not a public primitive derivation and not a full local-GR/PPN claim.
- The live local-GR work now moves to `A_MF`/EH principal-block ownership, the `E_00` Poisson residual, PPN side channels, common-`G` stationarity, and empirical material/R10 values.

## Owner Edge Activation

{markdown_table(owner_rows, ["edge_id", "edge_or_signature", "kills_or_controls", "activation_status", "remaining_guard"])}

## Private Source-Zero Propagation

{markdown_table(zero_rows, ["zero_id", "subvector", "private_branch_value", "status", "survivor"])}

## epsilon_Gsrc / Poisson Projection Inputs

{markdown_table(projection, ["projection_id", "arena", "projection_formula", "status"])}

## Live Residual Survivors

{markdown_table(survivors, ["survivor_id", "residual_family", "observable_targets", "current_status", "next_action"])}

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

    formal = f"""# PPC4161 4758: Owner/no-wA Activation and epsilon_Gsrc Projection Rebase

Generated: `{timestamp}`

## Branch-Reconciled Source Coupling State

The private PPC4161 GR-parity standard-matter import branch adopts

```text
S_matter = one imported scalar density functor
Hom(SpeciesLabel or MaterialLabel, Coeff_active_source)=empty
variation before source/test readout.
```

Therefore, inside that private branch,

```text
Delta_w_A = 0,
material_active_source_reentry = 0.
```

This closes the main source-weight `w_A` leg privately, not publicly.

## Common-G Owner Law

The 4718 action signature gives

```text
S_parent = S_geo[Phi] + S_MTS_aux[Phi]
         + lambda_D S_matter[Psi; e_obs(q(Phi)), omega(e_obs), A_Q(q(Phi)), theta_rep]
         + S_boundary
```

and, if the metric sector has the EH limit,

```text
M_EH^2 G_mu_nu = lambda_D T_mu_nu + R_mu_nu^local,
G_eff = lambda_D/(8*pi*M_EH^2).
```

## Poisson Projection

With

```text
E_mu_nu = R_mu_nu^local/M_EH^2,
kappa_eff = lambda_D/M_EH^2,
```

the static slow-source limit is

```text
nabla^2 Phi_N = 4*pi*G_eff*rho + (c^2/2)E_00.
```

Thus a density-region Newton residual is

```text
epsilon_N <= |E_00|/(kappa_eff rho c^2)
           + |delta_source|
           + |Delta_Lambda|/(4*pi*G_eff rho)
           + |Delta_boundary|/(4*pi*G_eff rho).
```

The zero-monopole source-shape branch remains

```text
E_perp <= delta_N/K_N(s),
K_N(s)=min((1-s)^-2, 2s(1-s)^-3).
```

## Live Bottleneck

The coupling source-weight gremlin is no longer the main private-branch blocker. The next hard target is:

```text
A_MF / EH principal block ownership  OR  source-backed E_00 residual coefficient bound.
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4758 reconciles 4757 with the later 4446/4447 and 4718/4719 chain.
- Inside the private PPC4161 GR-parity standard-matter import branch, `Delta_w_A=0` and material active-source reentry `=0`.
- This does not prove a public primitive Standard Model/no-source-prefactor theorem, and it does not close full local GR.
- The live blocker shifts to `A_MF`/EH principal-block ownership, `E_00` Poisson residual coefficients, PPN side channels, common-`G` stationarity and empirical material/R10 values.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4758 local packet update: do not keep circling `w_A` as if it is still wholly open. It is closed inside the private GR-parity import branch. The next serious route is the metric side: `A_MF`/EH principal block or a source-backed `E_00` residual coefficient.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4758-Y5-R2FR-owner-no-wA-edge-activation-or-epsilonGsrc-projection-inputs.md`

## Decision

`{DECISION}`

## What moved forward

- Reconciled the 4757 coupling fork with newer 4446/4447 private-branch source-universality work.
- Marked `Delta_w_A=0` and material active-source reentry `=0` inside the private GR-parity standard-matter import branch.
- Rebased the finite projection route onto the 4718/4719 common-`G` and Poisson residual equations.
- Moved the live local-GR target to `A_MF`/EH principal-block ownership or a source-backed `E_00` residual coefficient bound.

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
        "local_gr_source_coupling_private_activation",
        "4758 reconciles the owner/no-wA fork with 4446/4447: source-weight and material-reentry pieces are zero inside the private GR-parity import branch, while Poisson/PPN residuals remain explicit.",
        "Generated source register, owner-edge activation rows, private source-zero propagation rows, epsilonGsrc projection input rows, live survivor rows, route matrix, gates, firewalls, decision, status, next target and validation.",
        "private_GR_parity_source_weight_zero_Poisson_projection_nonclaim",
        NEXT_TARGET,
        "Treating private branch source-weight zero as public local-GR closure, numeric G_N prediction, or PPN/R10/WEP pass.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need A_MF/EH principal-block ownership or source-backed E00 residual coefficient bound.",
        "owner/no-wA edge activation or epsilonGsrc projection inputs",
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
    zero_rows: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4758_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4758_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4758_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4758_2_private_activation", "owner rows include private GR-parity activation and public guard", any(row["activation_status"] == "PRIVATE_BRANCH_ACTIVATED_BY_4446" for row in owner_rows) and any(row["activation_status"] == "NOT_ACTIVATED" for row in owner_rows), str(OWNER_EDGE_CSV)))
    checks.append(("VAL4758_3_source_zero", "source zero rows set Delta_w_A and material reentry to zero privately", any(row["zero_id"] == "SZ4758_0_Delta_w_A" and row["private_branch_value"] == "0" for row in zero_rows) and any(row["zero_id"] == "SZ4758_1_material_reentry" and row["private_branch_value"] == "0" for row in zero_rows), str(SOURCE_ZERO_CSV)))
    checks.append(("VAL4758_4_projection", "projection rows include G_eff, Poisson E_00 and K_N(s)", any("G_eff=lambda_D" in row["projection_formula"] for row in projection) and any("E_00" in row["projection_formula"] and "nabla^2 Phi_N" in row["projection_formula"] for row in projection) and any("K_N(s)" in row["projection_formula"] for row in projection), str(PROJECTION_CSV)))
    checks.append(("VAL4758_5_survivors", "survivor map includes A_MF/EH and E_00 targets", any("A_MF" in row["residual_family"] for row in survivors) and any("E_00" in row["residual_family"] for row in survivors), str(SURVIVOR_CSV)))
    checks.append(("VAL4758_6_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4758_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4758_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4758_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4758_10_claim_row", "claim row L-600 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4758_11_resume", "resume points from 4758 to 4759", "4758-Y5" in resume_text and "4759-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4758_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4758_OVERALL",
            "check": "all 4758 private source-coupling activation and projection checks pass",
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
    owner_rows = owner_edge_rows(timestamp)
    zero_rows = source_zero_rows(timestamp)
    projection = projection_rows(timestamp)
    survivors = survivor_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(OWNER_EDGE_CSV, owner_rows)
    write_csv(SOURCE_ZERO_CSV, zero_rows)
    write_csv(PROJECTION_CSV, projection)
    write_csv(SURVIVOR_CSV, survivors)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, owner_rows, zero_rows, projection, survivors, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, owner_rows, zero_rows, projection, survivors, gates, timestamp))


if __name__ == "__main__":
    main()
