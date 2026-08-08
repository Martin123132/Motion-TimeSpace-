from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT_DIR = POST / "source-intake" / "functional_rg" / "4936"
OUTPUT = OUTPUT_DIR / "O4_functional_trace_projection_results.json"
TABLE_OUTPUT = OUTPUT_DIR / "O4_source_channel_projection.csv"

SIX_DERIVATIVE = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
BASIS = POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv"
MOTION_TABLE = POST / "source-intake" / "functional_rg" / "4935" / "motion_sector_entry_operator_table.csv"
FRACTIONAL_FLOW = OUTPUT_DIR / "fractional_potential_LPA_closure_results.json"
SOURCE_FLOW = OUTPUT_DIR / "scalar_source_flow_evaluation_results.json"

MARKER = "MTS_4936_O4_FUNCTIONAL_TRACE_PROJECTION"
EXPECTED_HASHES = {
    SIX_DERIVATIVE: "1b987f0040d4288d9057b52f2f792c6484b6a0a8edd0bf817d71f7abf6a03755",
    BASIS: "93d8485ad79cc72ce2e9f6be3d81dc3605c785cb45436431d64041415e951361",
    MOTION_TABLE: "50f6a5481e3e1a94df12469ce13fa0a88450770a5930226eec928f8e9bafc3d6",
    FRACTIONAL_FLOW: "8af1d8bf764372917991126c86de63847714f1a48ca4f5eb0925d1b91a4fdf96",
    SOURCE_FLOW: "ab7394cf0ea455b40ec8678f5bb5cf34025657a51af499b5e92825b993dd6359",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    hash_failures = {
        path.as_posix(): {"expected": expected, "actual": digest(path)}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if hash_failures:
        raise RuntimeError(f"O4 projection source hash mismatch: {hash_failures}")

    basis_rows = read_csv(BASIS)
    o4_rows = [row for row in basis_rows if row["operator_id"] == "S6_O4"]
    motion_rows = read_csv(MOTION_TABLE)
    motion_o4_rows = [row for row in motion_rows if row["entry_id"] == "ME4935_03_O4_portal"]
    if len(o4_rows) != 1 or len(motion_o4_rows) != 1:
        raise RuntimeError("source-locked O4 operator is not unique")

    psi = sp.symbols("psi", positive=True)
    g_psi = sp.symbols("g_psi", positive=True)
    u_o4, curvature_squared, momentum_squared = sp.symbols(
        "u_O4 C2 p2", real=True
    )
    potential_hessian = g_psi / (3 * psi ** sp.Rational(2, 3))
    first_background_derivative = sp.diff(potential_hessian, psi)
    second_background_derivative = sp.diff(potential_hessian, psi, 2)
    o4_two_point_kernel = 2 * u_o4 * curvature_squared * momentum_squared
    o4_projector = sp.simplify(
        sp.diff(
            sp.diff(o4_two_point_kernel, momentum_squared), curvature_squared
        )
        / 2
    )

    source_flow = json.loads(SOURCE_FLOW.read_text(encoding="utf-8"))
    additive_source = sp.sympify(
        source_flow["derived_source_channels"]["leading_additive_gravity_source"]
    )
    fractional_flow = json.loads(FRACTIONAL_FLOW.read_text(encoding="utf-8"))

    channel_rows = [
        {
            "channel_id": "O4_4936_00_projector",
            "trace_block": "definition",
            "background_requirement": "locally constant nonzero Weyl-squared plus nonzero scalar momentum",
            "exact_result": "P_O4=(1/2) partial_(C^2) partial_(p^2) Gamma_psi_psi^(2)|_(p^2=C^2=0)",
            "additive_O4_source": "not applicable",
            "status": "PROJECTOR_DERIVED",
            "reason": "the O4 Hessian is 2u_O4 C^2 p^2 on the local projection background",
        },
        {
            "channel_id": "O4_4936_01_free_scalar_diagonal",
            "trace_block": "Tr[(P_psi+R_k)^(-1) partial_t R_k] with P_psi=-Box",
            "background_requirement": "free shift-symmetric scalar; regulator independent of background psi",
            "exact_result": "delta^2 trace/delta psi delta psi=0",
            "additive_O4_source": "0",
            "status": "ZERO_PROVED",
            "reason": "the complete scalar trace depends on the metric but not on the background scalar, so every projector containing scalar variations annihilates it",
        },
        {
            "channel_id": "O4_4936_02_fractional_scalar_diagonal",
            "trace_block": "P_psi=-Box+E(psi), E=V''",
            "background_requirement": "nonzero smooth scalar background before taking the vacuum limit",
            "exact_result": f"E'={first_background_derivative}; E''={second_background_derivative}",
            "additive_O4_source": "not identically zero; finite constant coefficient not defined at psi=0",
            "status": "NONZERO_CHANNEL_VACUUM_PROJECTOR_SINGULAR",
            "reason": "the second scalar variation contains G E' G E' G dotR and -G E'' G dotR terms, while E' and E'' diverge at the parent vacuum",
        },
        {
            "channel_id": "O4_4936_03_gravity_motion_mixed",
            "trace_block": "full block Hessian or scalar Schur complement P_psipsi-P_psih P_hh^(-1) P_hpsi",
            "background_requirement": "curved background and scalar momentum/gradient",
            "exact_result": "primary-source four-derivative comparator has beta_Dphi4(g,0)=(406/5)g^2+O(g^3)",
            "additive_O4_source": "allowed and generically nonzero; six-derivative coefficient not supplied by the comparator",
            "status": "CHANNEL_NONZERO_PROVED_COEFFICIENT_REQUIRES_SIX_DERIVATIVE_TRACE",
            "reason": "executed source flow proves gravity generates scalar interactions even when their coupling is zero",
        },
        {
            "channel_id": "O4_4936_04_O4_self_insertion",
            "trace_block": "P_psi includes -2u_O4 nabla_mu(C^2 nabla^mu)",
            "background_requirement": "nonzero Weyl-squared projection background",
            "exact_result": "Gamma_psi_psi^(2) contains 2u_O4 C^2 p^2",
            "additive_O4_source": "proportional to u_O4 and therefore not additive at u_O4=0",
            "status": "MULTIPLICATIVE_CHANNEL_DERIVED",
            "reason": "this channel controls canonical running and self-mixing but cannot create O4 from zero",
        },
    ]
    for row in channel_rows:
        row["valid_for_claim"] = False
        row["checkpoint_marker"] = MARKER

    checks = {
        "source_basis_has_unique_O4": len(o4_rows) == 1,
        "motion_entry_has_unique_O4": len(motion_o4_rows) == 1,
        "projector_recovers_uO4": o4_projector == u_o4,
        "fractional_E_prime_exact": first_background_derivative
        == -2 * g_psi / (9 * psi ** sp.Rational(5, 3)),
        "fractional_E_double_prime_exact": second_background_derivative
        == 10 * g_psi / (27 * psi ** sp.Rational(8, 3)),
        "fractional_E_prime_vacuum_diverges": sp.limit(
            first_background_derivative, psi, 0, dir="+"
        )
        == -sp.oo,
        "fractional_E_double_prime_vacuum_diverges": sp.limit(
            second_background_derivative, psi, 0, dir="+"
        )
        == sp.oo,
        "executed_source_additive_channel_is_406_over_5": additive_source
        == sp.Rational(406, 5),
        "fractional_one_coupling_closure_is_false": fractional_flow[
            "claim_boundary"
        ]["fractional_one_coupling_LPA_closed"]
        is False,
        "no_channel_row_claims_O4_coefficient": all(
            row["valid_for_claim"] is False for row in channel_rows
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(f"O4 projection checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "operator": {
            "definition": "S_O4=u_O4 integral sqrt(g) C_{abcd}C^{abcd} nabla_mu psi nabla^mu psi",
            "position_space_Hessian": "-2u_O4 nabla_mu[C^2 nabla^mu]",
            "local_momentum_kernel": str(o4_two_point_kernel),
            "projector": "P_O4=(1/2)partial_(C^2)partial_(p^2) Gamma_psi_psi^(2)",
            "projector_test": str(o4_projector),
        },
        "free_scalar_zero_theorem": {
            "assumptions": [
                "P_psi=-Box_g is independent of the background scalar",
                "R_k is a function of the metric Laplacian and not of background psi",
                "u_O4=0 and there is no gravity-scalar Hessian mixing in the isolated trace",
            ],
            "result": "P_O4 Tr[(P_psi+R_k)^(-1)partial_t R_k]=0 exactly",
            "scope": "isolated free scalar diagonal trace only",
        },
        "fractional_scalar_result": {
            "E": str(potential_hessian),
            "E_prime": str(first_background_derivative),
            "E_double_prime": str(second_background_derivative),
            "second_variation_structure": "Tr[G E' delta_1psi G E' delta_2psi G dotR]+(1<->2)-Tr[G E'' delta_1psi delta_2psi G dotR], all with the overall Wetterich 1/2 factors",
            "result": "the scalar diagonal source is no longer zero, but its vacuum O4 projector is singular for the bare fractional potential",
            "required_repair": "use the renormalized smooth finite-k potential and a field-dependent O4 coefficient u_O4(psi), or prove an exact mixed-trace cancellation before taking psi to zero",
        },
        "mixed_gravity_result": {
            "executed_lower_order_comparator": "beta_Dphi4(g,0)=(406/5)g^2+O(g^3)",
            "deduction": "gravity-motion mixing is a proved additive source channel, not an optional closure assumption",
            "boundary": "the six-derivative C^2 p^2 coefficient still requires the corresponding curved-background functional trace",
        },
        "channel_rows": channel_rows,
        "checks": checks,
        "claim_boundary": {
            "O4_projector_derived": True,
            "free_scalar_additive_O4_source_zero_proved": True,
            "fractional_scalar_O4_vacuum_projection_finite": False,
            "gravity_motion_additive_channel_proved": True,
            "numeric_O4_beta_coefficient_derived": False,
            "full_MTS_trajectory_calculated": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(TABLE_OUTPUT, channel_rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_TABLE_SHA256={digest(TABLE_OUTPUT)}", flush=True)
    print(f"{MARKER}_PROJECTOR={o4_projector}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
