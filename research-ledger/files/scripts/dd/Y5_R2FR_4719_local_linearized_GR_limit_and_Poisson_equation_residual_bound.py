from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4719"
CLAIM_ID = "L-561"
MARKER = "PPC4161_LOCAL_LINEARIZED_GR_LIMIT_AND_POISSON_RESIDUAL_BOUND_4719"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_LINEARIZED_GR_LIMIT_AND_POISSON_RESIDUAL_BOUND_4719"
DECISION = "LINEARIZED_GR_POISSON_BRIDGE_DERIVED_CONDITIONALLY_RESIDUAL_VECTOR_EXPLICIT_NONCLAIM"
NEXT_TARGET = "4720-Y5-R2FR-EH-reduction-parent-signature-or-nonEH-operator-coefficient-matrix.md"

DOC_PATH = POST / "4719-Y5-R2FR-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md"
FORMAL_PATH = FORMAL / "735-PPC4161-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_SOURCE_REGISTER.csv"
LINEARIZED_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_LINEARIZED_FIELD_EQUATION_ROWS.csv"
POISSON_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_POISSON_RESIDUAL_BOUND_ROWS.csv"
PPN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_PPN_RESIDUAL_VECTOR_ROWS.csv"
RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_RESIDUAL_CLOSURE_GATES.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4719_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4719_VALIDATION.csv"


SOURCE_SPECS = [
    {
        "source_id": "SRC4719_0",
        "path": "P8_Y5_R2FR_4718_COMMON_G_NORMALIZATION_OWNER_ROWS.csv",
        "needle": "GNL4718_0_Einstein_coupling_law",
        "role": "Current common-coupling owner law G_eff=lambda_D/(8*pi*M_EH^2).",
    },
    {
        "source_id": "SRC4719_1",
        "path": "P8_Y5_R2FR_4718_COMMON_G_NORMALIZATION_OWNER_ROWS.csv",
        "needle": "GNL4718_1_Newton_Poisson_limit",
        "role": "4718 target that asked for a Poisson residual bound.",
    },
    {
        "source_id": "SRC4719_2",
        "path": "P8_Y5_R2FR_4718_LOCAL_GR_NEWTON_RESIDUAL_ROWS.csv",
        "needle": "RLG4718_1_Newton_residual",
        "role": "Residual envelope that 4719 refines into normalized Poisson/PPN rows.",
    },
    {
        "source_id": "SRC4719_3",
        "path": "P8_Y5_R2FR_4171_WEAK_FIELD_READOUT.csv",
        "needle": "WF4171_3_EH_linear",
        "role": "Older weak-field identity G_00^lin=2 nabla^2 Phi_N/c^2.",
    },
    {
        "source_id": "SRC4719_4",
        "path": "P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION.csv",
        "needle": "PG4171_2_poisson",
        "role": "Older Poisson/Gauss/Newton readout to be rebased onto lambda_D/M_EH^2.",
    },
    {
        "source_id": "SRC4719_5",
        "path": "P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT.csv",
        "needle": "OR4171_2_radial",
        "role": "Slow-orbit Newtonian acceleration readout after the Poisson equation.",
    },
    {
        "source_id": "SRC4719_6",
        "path": "P8_Y5_R2FR_4172_PPN_GAUGE_AND_ASSUMPTIONS.csv",
        "needle": "GAUGE4172_2_g00",
        "role": "PPN metric convention for g00 and beta.",
    },
    {
        "source_id": "SRC4719_7",
        "path": "P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION.csv",
        "needle": "Gdot_over_G",
        "role": "Full private PPN residual vector including coupling drift.",
    },
    {
        "source_id": "SRC4719_8",
        "path": "P8_Y5_R2FR_4278_LEFT_HAND_EH_NEWTON_DERIVATION.csv",
        "needle": "LHD4278_4_Poisson_readout",
        "role": "Left-hand EH/Newton gate assembling conditional Poisson readout.",
    },
    {
        "source_id": "SRC4719_9",
        "path": "P8_Y5_R2FR_4278_RESIDUAL_EFT_COEFFICIENT_MAP.csv",
        "needle": "RES4278_1_curvature_squared",
        "role": "Non-EH residual coefficient map that must be bounded if not zero.",
    },
    {
        "source_id": "SRC4719_10",
        "path": "MTS_local_residual_predictions_TEMPLATE.csv",
        "needle": "R3_gamma",
        "role": "Local residual prediction template warning that Poisson alone does not prove gamma.",
    },
    {
        "source_id": "SRC4719_11",
        "path": "P8_Y5_R2FR_4717_DELTAW_KERNEL_FIRST_ROWS.csv",
        "needle": "DWK4717_2_PPN_source_vector",
        "role": "Source-prefactor contribution to the PPN residual vector.",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    path.write_text(existing + separator + block.rstrip() + "\n", encoding="utf-8", newline="\n")


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = SOURCE_DIR / spec["path"]
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(path),
                "exists": path.exists(),
                "needle": spec["needle"],
                "needle_found": spec["needle"] in text,
                "role": spec["role"],
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def linearized_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LFE4719_0_parent_field_equation",
            "statement": "Start from the 4718 bridge M_EH^2 G_mu_nu[g_eff]=lambda_D T_mu_nu+R_mu_nu^local.",
            "derivation": "Divide by M_EH^2 and define kappa_eff=lambda_D/M_EH^2=8*pi*G_eff/c^4, E_mu_nu=R_mu_nu^local/M_EH^2.",
            "output": "G_mu_nu=kappa_eff T_mu_nu+E_mu_nu.",
            "status": "derived_from_4718_signature",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LFE4719_1_linearized_harmonic_gauge",
            "statement": "Let g_eff=eta+h, trace reverse bar_h_mu_nu=h_mu_nu-1/2 eta_mu_nu h, and impose partial^mu bar_h_mu_nu=0.",
            "derivation": "The EH principal block gives G_mu_nu^(1)=-1/2 box bar_h_mu_nu.",
            "output": "box bar_h_mu_nu=-2 kappa_eff T_mu_nu-2 E_mu_nu plus higher-order/non-EH terms.",
            "status": "standard_EH_linear_identity_rebased",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LFE4719_2_static_slow_source",
            "statement": "For a static slow source T_00=rho c^2+O(v^2/c^2), T_0i small, and g_00=-(1+2 Phi_N/c^2)+O(c^-4).",
            "derivation": "The 00 Einstein identity is G_00^(1)=2 nabla^2 Phi_N/c^2 in the same observed metric frame used by 4171.",
            "output": "2 nabla^2 Phi_N/c^2=kappa_eff rho c^2+E_00.",
            "status": "Poisson_parent_equation",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LFE4719_3_Poisson_equation_with_residual",
            "statement": "Substitute kappa_eff=8*pi*G_eff/c^4.",
            "derivation": "Multiplying the 00 equation by c^2/2 gives the Newtonian source equation with an additive residual.",
            "output": "nabla^2 Phi_N=4*pi*G_eff*rho+(c^2/2)E_00.",
            "status": "derived_conditionally",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LFE4719_4_Gauss_orbit_readout",
            "statement": "If E_00 is negligible or bounded and the exterior is compact/asymptotically flat, Gauss gives Phi_N=-G_eff M_H/r plus multipoles.",
            "derivation": "Integrating the Poisson equation over a compact source gives int grad Phi_N dot dS=4*pi*G_eff M_H+(c^2/2)int E_00 dV.",
            "output": "a=-grad Phi_N and a_r=-G_eff M_H/r^2 plus residual force.",
            "status": "orbital_readout_conditional",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def poisson_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "PB4719_0_absolute_source_residual",
            "quantity": "Delta_Poisson_abs",
            "formula": "|Delta(nabla^2 Phi_N)| <= (c^2/2)|E_00| + 4*pi*G_eff*rho*|delta_source| + |Delta_Lambda| + |Delta_boundary|",
            "meaning": "Absolute deviation from the GR/Newton Poisson source.",
            "zero_condition": "E_00=0, relative source prefactors zero, local Lambda negligible/absorbed, boundary flux silent.",
            "claim_state": "bound_contract_not_numeric",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "PB4719_1_fractional_density_region",
            "quantity": "epsilon_N_density",
            "formula": "epsilon_N <= |E_00|/(kappa_eff rho c^2) + |delta_source| + |Delta_Lambda|/(4*pi*G_eff rho) + |Delta_boundary|/(4*pi*G_eff rho)",
            "meaning": "Dimensionless Newton-source residual where rho is nonzero.",
            "zero_condition": "all numerator terms vanish or are below local Newton/PPN sensitivity.",
            "claim_state": "ready_for_numeric_coefficients",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "PB4719_2_exterior_force_residual",
            "quantity": "epsilon_a_exterior",
            "formula": "|Delta a_r|/|G_eff M_H/r^2| <= |int E_00 dV|/(kappa_eff M_H c^2) + |delta_M_H|/M_H + |multipoles|/(M_H r^l) + |boundary_flux|/(G_eff M_H)",
            "meaning": "Exterior inverse-square residual; orbital GM is not used as an input.",
            "zero_condition": "same Hamiltonian/Hilbert source charge, compact monopole branch, no boundary/source flux.",
            "claim_state": "ready_for_orbital_gate",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "PB4719_3_common_G_drift",
            "quantity": "dotG_eff_over_G_eff",
            "formula": "D_tau ln G_eff = D_tau ln lambda_D - D_tau ln M_EH^2",
            "meaning": "Universal coupling drift is separate from relative source coupling.",
            "zero_condition": "lambda_D and M_EH^2 are constants/superselection labels or share a parent identity.",
            "claim_state": "Gdot_gate_needed",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def ppn_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "ppn_id": "PPNV4719_0_gamma",
            "component": "gamma_minus_1",
            "residual_formula": "gamma-1 = Pi_gamma[E_ij^TF, c_D, c_R2/M_R, c_Gamma, Delta_Hodge_light, boundary_TF]",
            "closure_condition": "EH spatial equation in the same observed metric; no scalar/disformal/spatial hidden channel.",
            "why_poisson_not_enough": "The 00 Poisson equation fixes the Newton potential source but not the spatial curvature per unit U.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "ppn_id": "PPNV4719_1_beta",
            "component": "beta_minus_1",
            "residual_formula": "beta-1 = Pi_beta[E_00^(2), nonlinear_EH_coefficient_error, delta_kappa, binding_stress_double_count]",
            "closure_condition": "EH nonlinear self-interaction coefficient and same Hilbert source through 2PN.",
            "why_poisson_not_enough": "First-order Newton recovery does not fix the U^2 coefficient in g_00.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "ppn_id": "PPNV4719_2_preferred_frame",
            "component": "alpha1_alpha2_alpha3_xi",
            "residual_formula": "||alpha_xi|| <= Pi_vec[vector/torsion slots, q-frame drift, anisotropic projector, external memory gradient, boundary momentum flux]",
            "closure_condition": "single observed coframe, no representative velocity field, Bianchi-owned total stress, compact boundary silence.",
            "why_poisson_not_enough": "Scalar Newton potential recovery does not rule out vector/aniso/preferred-frame side channels.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "ppn_id": "PPNV4719_3_conservation",
            "component": "zeta1_zeta2_zeta3_zeta4",
            "residual_formula": "||zeta|| <= Pi_zeta[div E_mu_nu, source_prefactor_delta_w, EM/Poynting owner defects, boundary/source exchange]",
            "closure_condition": "nabla_mu(T_total^mu_nu)=0 from parent variation, same EM/Hilbert stress, no source-only weights.",
            "why_poisson_not_enough": "A correct static source strength does not prove full stress-energy conservation.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "ppn_id": "PPNV4719_4_Gdot",
            "component": "Gdot_over_G",
            "residual_formula": "Gdot/G = D_tau ln(lambda_D/M_EH^2) + readout_tau_tail",
            "closure_condition": "common scale and EH kinetic normalization are stationary parent constants or share a cancelling identity.",
            "why_poisson_not_enough": "Instantaneous Newton recovery still allows time drift unless the common normalization is owned.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def residual_gate_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "RCG4719_0_EH_principal_block",
            "residual": "E_EH_closure",
            "requirement": "q-basic metric sector has EH principal block through 2PN.",
            "effect_if_unsigned": "Poisson and PPN become closure-only with non-EH coefficient matrix.",
            "passed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "RCG4719_1_same_source_charge",
            "residual": "delta_source",
            "requirement": "rho is the same Hamiltonian/Hilbert source charge before orbital readout.",
            "effect_if_unsigned": "GM can be fitted but not derived from source charge.",
            "passed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "RCG4719_2_source_prefactor_zero",
            "residual": "delta_w, Delta_kappa, q_A",
            "requirement": "4717 parent signature is signed or finite kernels are filled.",
            "effect_if_unsigned": "WEP/R10/PPN source coupling channels remain live.",
            "passed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "RCG4719_3_boundary_projection_silence",
            "residual": "boundary_flux, multipoles, local projector tails",
            "requirement": "compact source/no-flux collar or explicit exterior multipole bound.",
            "effect_if_unsigned": "inverse-square and alpha3/preferred-frame channels remain bounded, not closed.",
            "passed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "RCG4719_4_common_G_stationarity",
            "residual": "D_tau ln(lambda_D/M_EH^2)",
            "requirement": "common matter scale and metric kinetic scale are constants or linked by parent identity.",
            "effect_if_unsigned": "Gdot/orbital/clock drift gate remains open.",
            "passed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def promotion_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "promotion_id": "PROM4719_0_Newton_private",
            "target": "Newtonian Poisson/inverse-square recovery",
            "needed": "All Poisson residual gates close or numeric residuals pass source-backed local bounds.",
            "current_result": "conditional equation derived, residual bound explicit, not promoted.",
            "promoted": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "promotion_id": "PROM4719_1_PPN_private",
            "target": "Full local GR/PPN recovery",
            "needed": "gamma, beta, alpha_i, xi, zeta_i, and Gdot rows close in one shared convention.",
            "current_result": "residual vector staged; no full PPN score claimed.",
            "promoted": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "promotion_id": "PROM4719_2_numeric_G",
            "target": "Numerical G_N derivation",
            "needed": "lambda_D and M_EH^2 derived from MTS primitives, not calibrated.",
            "current_result": "owner relation derived; numerical value not predicted.",
            "promoted": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4719_0_no_poisson_to_full_GR_shortcut",
            "rule": "Do not use the Poisson equation alone as a local-GR/PPN pass.",
            "reason": "Gamma, beta, preferred-frame, conservation, and Gdot rows remain separate.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4719_1_no_numeric_G_claim",
            "rule": "Do not claim the numerical value of G_N is derived.",
            "reason": "4719 derives G_eff ownership and Poisson structure only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4719_2_no_orbital_GM_backfill",
            "rule": "Orbital GM must be a downstream test, not an input defining the source charge.",
            "reason": "The source is the Hamiltonian/Hilbert charge with residual gates.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4719_0",
            "decision": DECISION,
            "meaning": "The local GR/Newton route now has a clean weak-field equation in the current coupling language: nabla^2 Phi_N=4*pi G_eff rho+(c^2/2)E_00. The price is explicit: E_00 and the PPN side channels must be zero or bounded; no full local-GR claim fires from Poisson alone.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4719_0",
            "status": "private_nonclaim_linearized_GR_bridge",
            "summary": "Linearized EH bridge, Poisson equation, exterior acceleration residual, and PPN residual vector derived conditionally in the 4718 lambda_D/M_EH^2 coupling language.",
            "claim_allowed": False,
            "timestamp_utc": ts,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4719_0",
            "next_target": NEXT_TARGET,
            "why": "The weak-field math now says exactly what must be zero or bounded; the next leverage point is the EH reduction itself or, failing that, a non-EH coefficient matrix feeding R10/PPN/orbital gates.",
            "derive_first": "prove the parent metric sector reduces to the EH principal block through 2PN with no independent R^2/Ricci^2/Weyl^2/torsion/disformal/memory operator in local matter collars",
            "fallback": "fill a non-EH operator coefficient matrix with units, source paths, projection kernels, and local test bounds",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def write_docs(
    ts: str,
    sources: list[dict[str, Any]],
    linearized: list[dict[str, Any]],
    poisson: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    source_lines = "\n".join(
        f"- `{r['source_id']}`: `{r['source_path']}`; exists={r['exists']}; needle_found={r['needle_found']}; role={r['role']}"
        for r in sources
    )
    lin_lines = "\n".join(f"- `{r['row_id']}`: {r['output']} Status: `{r['status']}`." for r in linearized)
    pois_lines = "\n".join(f"- `{r['bound_id']}` / `{r['quantity']}`: `{r['formula']}`" for r in poisson)
    ppn_lines = "\n".join(f"- `{r['ppn_id']}` / `{r['component']}`: `{r['residual_formula']}`" for r in ppn)
    gate_lines = "\n".join(f"- `{r['gate_id']}` / `{r['residual']}`: passed={r['passed']}; {r['requirement']}" for r in gates)

    write_text(
        DOC_PATH,
        f"""# 4719 - Local Linearized GR Limit and Poisson Equation Residual Bound

Generated: `{ts}`

## Purpose

This checkpoint rebases the older 4171/4172/4278 Newton/PPN branch onto the newer 4718 coupling owner law:

`G_eff = lambda_D/(8*pi*M_EH^2)`.

The aim is to derive the weak-field bridge rather than merely assert that MTS should reduce to GR.

## Main Derivation

Start from:

`M_EH^2 G_mu_nu[g_eff] = lambda_D T_mu_nu + R_mu_nu^local`

Define:

`kappa_eff = lambda_D/M_EH^2 = 8*pi*G_eff/c^4`

and:

`E_mu_nu = R_mu_nu^local/M_EH^2`.

Then:

`G_mu_nu = kappa_eff T_mu_nu + E_mu_nu`.

In harmonic gauge with `g_eff=eta+h`, the EH block gives:

`G_mu_nu^(1) = -1/2 box bar_h_mu_nu`.

For a static slow source:

`T_00 = rho c^2`, `g_00=-(1+2 Phi_N/c^2)`, and `G_00^(1)=2 nabla^2 Phi_N/c^2`.

Therefore:

`nabla^2 Phi_N = 4*pi*G_eff*rho + (c^2/2)E_00`.

That is the clean local Newton bridge in the current MTS language.

## What This Actually Buys

This is a forward step:

- `G` is no longer an unowned mystery knob in this branch; it is the ratio `lambda_D/M_EH^2`.
- Newton's Poisson equation follows if the EH principal block and source signature are signed.
- The residual is explicit: `(c^2/2)E_00` plus source, boundary, multipole, drift, and non-EH tails.
- Poisson alone still does not prove full local GR; the PPN vector is retained separately.

## Linearized Rows

{lin_lines}

## Poisson Bounds

{pois_lines}

## PPN Residual Vector

{ppn_lines}

## Closure Gates

{gate_lines}

## Source Register

{source_lines}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
""",
    )

    write_text(
        FORMAL_PATH,
        f"""# PPC4161 4719 - Local Linearized GR Limit and Poisson Residual Bound

Generated: `{ts}`

## Formal Result

From the 4718 parent bridge:

`M_EH^2 G_mu_nu = lambda_D T_mu_nu + R_mu_nu^local`

define:

`E_mu_nu=R_mu_nu^local/M_EH^2`, `kappa_eff=lambda_D/M_EH^2=8*pi*G_eff/c^4`.

The weak-field 00 equation gives:

`nabla^2 Phi_N = 4*pi*G_eff rho + (c^2/2)E_00`.

Equivalently, where `rho != 0`:

`epsilon_N <= |E_00|/(kappa_eff rho c^2) + |delta_source| + |Delta_Lambda|/(4*pi*G_eff rho) + |Delta_boundary|/(4*pi*G_eff rho)`.

## PPN Separation

The Poisson equation controls only the scalar first-order Newton source. Full local GR still requires:

`Delta_PPN=(gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)`

to vanish or pass source-backed bounds in the same observed frame.

## Decision

`{DECISION}`

## Next

`{NEXT_TARGET}`
""",
    )


def update_claims(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if CLAIM_ID in {row.get("claim_id", "") for row in rows}:
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4719 conditionally derives the local linearized GR/Poisson bridge in the current lambda_D/M_EH^2 language and makes the Poisson plus PPN residual vector explicit.",
        "current_evidence": "Generated source register, linearized field-equation rows, Poisson residual bounds, PPN residual vector, closure gates, promotion gates, firewalls, decision, status, next target and validation.",
        "status": "conditional_linearized_GR_bridge_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating first-order Poisson recovery as full local-GR/PPN recovery or hiding non-EH coefficients inside calibrated G_eff.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "Local linearized GR limit and Poisson residual bound",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=fieldnames).writerow(new_row)


def update_resume(ts: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`4719-Y5-R2FR-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md`

## Decision

`{DECISION}`

## What moved forward

- The 4718 coupling owner law has been pushed into the weak-field equation.
- The local Newton bridge is now:

`nabla^2 Phi_N = 4*pi*G_eff*rho + (c^2/2)E_00`

where `G_eff=lambda_D/(8*pi*M_EH^2)` and `E_mu_nu=R_mu_nu^local/M_EH^2`.

- Poisson/Newton recovery is conditional on bounding or killing `E_00`, source-prefactor, boundary, multipole, and common-G drift terms.
- Full local GR still needs the PPN vector, not just the Poisson equation.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def validation_rows(
    ts: str,
    sources: list[dict[str, Any]],
    linearized: list[dict[str, Any]],
    poisson: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4719_sources_exist", all(r["exists"] for r in sources), "all cited local source paths exist"),
        ("VAL4719_needles_found", all(r["needle_found"] for r in sources), "all cited source needles found"),
        ("VAL4719_linearized_bridge", any(r["row_id"] == "LFE4719_3_Poisson_equation_with_residual" for r in linearized), "Poisson equation with residual derived"),
        ("VAL4719_Geff_language", any("G_eff" in r["output"] for r in linearized), "current G_eff language appears in linearized output"),
        ("VAL4719_poisson_bounds", len(poisson) >= 4 and any(r["bound_id"] == "PB4719_1_fractional_density_region" for r in poisson), "Poisson residual bounds present"),
        ("VAL4719_ppn_vector", len(ppn) >= 5 and any(r["ppn_id"] == "PPNV4719_0_gamma" for r in ppn), "PPN residual vector present"),
        ("VAL4719_closure_gates", len(gates) >= 5 and not all(bool(r["passed"]) for r in gates), "closure gates present and not all passing"),
        ("VAL4719_no_claim_allowed", all(not bool(r.get("valid_for_claim")) for r in sources + linearized + poisson + ppn + gates + promotions), "no row allows a claim"),
        ("VAL4719_no_promotions", not any(bool(r["promoted"]) for r in promotions), "no promotion rows are true"),
        ("VAL4719_doc_written", DOC_PATH.exists() and DOC_PATH.stat().st_size > 1000, "checkpoint document written"),
        ("VAL4719_formal_written", FORMAL_PATH.exists() and FORMAL_PATH.stat().st_size > 500, "formal packet document written"),
        ("VAL4719_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "passed": passed,
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4719_OVERALL",
            "passed": overall,
            "detail": "4719 artifacts validate as private nonclaim local linearized GR/Newton bridge",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()

    sources = source_register(ts)
    linearized = linearized_rows(ts)
    poisson = poisson_rows(ts)
    ppn = ppn_rows(ts)
    residual_gates = residual_gate_rows(ts)
    promotions = promotion_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(LINEARIZED_CSV, linearized)
    write_csv(POISSON_CSV, poisson)
    write_csv(PPN_CSV, ppn)
    write_csv(RESIDUAL_CSV, residual_gates)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    write_docs(ts, sources, linearized, poisson, ppn, residual_gates)
    update_claims(ts)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: the current `lambda_D/M_EH^2` coupling owner law now yields `nabla^2 Phi_N=4*pi*G_eff*rho+(c^2/2)E_00` in the weak-field limit.
- Still blocked: EH principal-block ownership, source-prefactor zero, boundary/projector silence, common-G stationarity and full PPN residual bounds.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: rebases the older Poisson/PPN ladder onto the current common-coupling owner law and makes the Newton/PPN residual vector explicit.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    update_resume(ts)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    write_csv(VALIDATION_CSV, validation_rows(ts, sources, linearized, poisson, ppn, residual_gates, promotions))


if __name__ == "__main__":
    main()
