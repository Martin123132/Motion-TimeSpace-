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

CHECKPOINT = "4720"
CLAIM_ID = "L-562"
MARKER = "PPC4161_EH_REDUCTION_PARENT_SIGNATURE_OR_NONEH_OPERATOR_MATRIX_4720"
PACKET_MARKER = "PPC4161_PACKET_EH_REDUCTION_PARENT_SIGNATURE_OR_NONEH_OPERATOR_MATRIX_4720"
DECISION = "EH_SELECTOR_THEOREM_CONDITIONAL_NONEH_OPERATOR_MATRIX_STAGED_NONCLAIM"
NEXT_TARGET = "4721-Y5-R2FR-two-derivative-EH-selector-proof-or-R2-scalar-range-bound-row.md"

DOC_PATH = POST / "4720-Y5-R2FR-EH-reduction-parent-signature-or-nonEH-operator-coefficient-matrix.md"
FORMAL_PATH = FORMAL / "736-PPC4161-EH-reduction-parent-signature-or-nonEH-operator-coefficient-matrix.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_SOURCE_REGISTER.csv"
SELECTOR_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_EH_SELECTOR_THEOREM_ROWS.csv"
SIGNATURE_CLAUSES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_PARENT_EH_SIGNATURE_CLAUSES.csv"
OPERATOR_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_NONEH_OPERATOR_COEFFICIENT_MATRIX.csv"
PROJECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_NONEH_PROJECTION_KERNEL_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4720_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4720_VALIDATION.csv"


SOURCE_SPECS = [
    {
        "source_id": "SRC4720_0",
        "path": "P8_Y5_R2FR_4719_RESIDUAL_CLOSURE_GATES.csv",
        "needle": "RCG4719_0_EH_principal_block",
        "role": "4719 identifies EH principal-block ownership as the next bottleneck.",
    },
    {
        "source_id": "SRC4720_1",
        "path": "P8_Y5_R2FR_4719_PPN_RESIDUAL_VECTOR_ROWS.csv",
        "needle": "PPNV4719_0_gamma",
        "role": "4719 separates Poisson from full PPN spatial-curvature recovery.",
    },
    {
        "source_id": "SRC4720_2",
        "path": "P8_Y5_R2FR_4719_POISSON_RESIDUAL_BOUND_ROWS.csv",
        "needle": "PB4719_1_fractional_density_region",
        "role": "4719 normalized Poisson residual that non-EH terms feed.",
    },
    {
        "source_id": "SRC4720_3",
        "path": "P8_Y5_R2FR_4278_LEFT_HAND_OPERATOR_GATE.csv",
        "needle": "OPG4278_1_effective_GR_residual_fork",
        "role": "4278 earlier fork from conditional EH to residual EFT coefficients.",
    },
    {
        "source_id": "SRC4720_4",
        "path": "P8_Y5_R2FR_4278_PALATINI_SELECTOR_CLAUSES.csv",
        "needle": "SEL4278_2_IR_two_derivative_order",
        "role": "IR/two-derivative selector clause for EH principal operator.",
    },
    {
        "source_id": "SRC4720_5",
        "path": "P8_Y5_R2FR_4278_RESIDUAL_EFT_COEFFICIENT_MAP.csv",
        "needle": "RES4278_1_curvature_squared",
        "role": "Residual EFT coefficient map for curvature-squared terms.",
    },
    {
        "source_id": "SRC4720_6",
        "path": "MTS_local_residual_predictions_TEMPLATE.csv",
        "needle": "R11_EH_operator_ledger",
        "role": "Local residual template requiring non-EH operator ledger rows.",
    },
    {
        "source_id": "SRC4720_7",
        "path": "P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv",
        "needle": "nonEH_operator_potential",
        "role": "Existing scorecard rows showing non-EH operator potential blocks gamma/beta/R10/R11.",
    },
    {
        "source_id": "SRC4720_8",
        "path": "R11_nonEH_operator_vector_executable.csv",
        "needle": "R2_fR_scalar_mode",
        "role": "Existing executable skeleton for non-EH operator family coefficients.",
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


def selector_theorem_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EHS4720_0_selector_theorem",
            "claim": "If the local visible geometry sector is single-metric/coframe, local, diffeomorphism and local-Lorentz covariant, parity-even, two-derivative, and has no propagating torsion/nonmetricity or extra scalar/vector coefficient target, the only principal bulk operator is Einstein-Hilbert plus Lambda/topological/boundary terms.",
            "derivation": "In a 4D local covariant low-energy action, two derivatives on the metric/coframe give the scalar curvature as the unique parity-even bulk scalar with second-order metric equations. The Palatini/EC form collapses to EH when torsion/nonmetricity are algebraic and zero/bounded. Lambda is zeroth order; Gauss-Bonnet/Euler is topological in 4D; boundary terms do not alter the bulk field equation under fixed boundary data.",
            "status": "conditional_sufficiency_theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EHS4720_1_what_it_kills",
            "claim": "The selector kills independent local R^2, Ricci^2, Weyl^2, scalar-tensor, vector/preferred-frame, disformal/second-metric, torsion/nonmetricity and memory-source operators at the principal local GR order.",
            "derivation": "Each survivor needs either more derivatives, an extra field/slot, a second metric/coframe, a local vector/selector, a nonlocal memory kernel, a boundary source term, or a source-only coefficient target. These are outside the signed selector and must be named coefficients if retained.",
            "status": "exact_if_selector_signed",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EHS4720_2_what_it_does_not_kill",
            "claim": "The selector does not derive the numerical value of M_EH, does not sign source coupling by itself, and does not close boundary/readout/local-test residuals.",
            "derivation": "EH uniqueness owns the left-hand operator. The coupling ratio lambda_D/M_EH^2, same-source charge, and local projection/no-flux gates remain distinct.",
            "status": "firewall",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EHS4720_3_verdict",
            "claim": "4720 converts the EH bottleneck into a real fork: sign the parent EH selector, or fill the non-EH coefficient matrix.",
            "derivation": "This is the shortest route under scrutiny because it uses standard uniqueness logic rather than tuning local-test coefficients. The fallback remains fully scoreable.",
            "status": "private_nonclaim_progress",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def signature_clause_rows(ts: str) -> list[dict[str, Any]]:
    clauses = [
        ("EHSC4720_0_single_geometry", "one observed metric/coframe is the only local matter/gravity geometry", "second metric/disformal leak", "c_D"),
        ("EHSC4720_1_local_covariant_4form", "bulk action is a local diffeo/Lorentz-covariant 4-form", "noncovariant projector force terms", "c_proj"),
        ("EHSC4720_2_two_derivative_IR", "principal local IR operator is two-derivative", "R2/Ricci2/Weyl2 higher-derivative modes", "c_R2_or_M_R"),
        ("EHSC4720_3_parity_even_no_vector", "no independent parity-odd or preferred-frame vector selector in compact local branch", "alpha_i/xi side channels", "c_vec"),
        ("EHSC4720_4_torsion_resolution", "torsion/nonmetricity are algebraic and vanish in compact spinless branch or are heavy/bounded", "torsion/nonmetricity preferred-frame and clock residuals", "c_T_or_c_Q"),
        ("EHSC4720_5_boundary_topological", "boundary/topological terms are fixed, source-blind, and do not create bulk source charge", "boundary mass/current hair", "c_bdy"),
        ("EHSC4720_6_no_memory_operator", "local collar has no independent Gamma/memory operator in the EH principal block", "range/local memory leakage", "c_Gamma"),
        ("EHSC4720_7_common_coupling_separate", "M_EH and lambda_D are common parent normalizations, not relative source coefficients", "source-prefactor hiding inside G", "delta_kappa_or_delta_w"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": clause_id,
            "clause": clause,
            "blocks": blocks,
            "fallback_coefficient": coeff,
            "parent_status": "unsigned_parent_clause",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for clause_id, clause, blocks, coeff in clauses
    ]


def operator_matrix_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("NEH4720_0_R2_fR_scalar", "c_R2_or_c_fR, M_R", "sqrt(-g)(c_R2 R^2 + c_fR f_extra(R))", "scalar finite-range mode; gamma/beta slip; R10 Yukawa alpha(lambda)", "R3_gamma;R4_beta;R10_fifth_force;R11", "prove absent by two-derivative selector or give M_R large/source-backed curve"),
        ("NEH4720_1_Ricci_Weyl_squared", "c_Ricci, c_Weyl", "sqrt(-g)(c_Ricci R_mn R^mn + c_Weyl C_mnrs C^mnrs)", "spin-2/higher-derivative slip; xi/tidal/wave-sector tails", "R3_gamma;R8_xi;R11", "topological reduction, heavy mass, or sourced EFT bound"),
        ("NEH4720_2_torsion_nonmetricity", "c_T, c_Q", "c_T T^2 + c_Q Q^2 plus spin/light-cone connection couplings", "preferred-frame, clock, WEP, light-cone residuals", "R0;R1;R2;R5;R6;R11", "algebraic zero in compact spinless branch or finite coefficient bound"),
        ("NEH4720_3_scalar_tensor", "F_phi, c_scalar", "sqrt(-g)[F(phi)R - 1/2(d phi)^2 - V(phi)]", "gamma/beta/Gdot/R10/clock residuals", "R2;R3;R4;R9;R10;R11", "no scalar target in parent or sourced scalar mass/coupling rows"),
        ("NEH4720_4_vector_preferred_frame", "c_vec", "u^mu, selector normal, domain velocity, or preferred-frame vector terms", "alpha1/alpha2/alpha3/xi", "R5;R6;R7;R8;R11", "no local vector selector theorem or numeric vector coefficient products"),
        ("NEH4720_5_second_metric_disformal", "c_D, b_dis", "matter/source sees g_tilde_mn=A^2 g_mn+B^2 v_m v_n", "WEP, gamma, clocks, fifth-force response", "R1;R2;R3;R10;R11", "same observed coframe theorem or canonical coupling bound"),
        ("NEH4720_6_memory_Gamma", "c_Gamma", "Gamma_eff/K_hat memory operator in local collar", "range-dependent local force; cosmology-local leakage; PPN drift", "R3;R4;R9;R10;R11", "double-zero/no-flux theorem or local profile coefficient bound"),
        ("NEH4720_7_boundary_charge", "c_bdy", "non-topological boundary/corner/source reference term", "source normalization, alpha3, orbital/clock drift", "R7;R9;R11;orbital", "fixed topological boundary or source-backed flux/no-hair bound"),
        ("NEH4720_8_Lambda_local", "Lambda_eff_local", "zeroth-order local vacuum term", "constant/tidal acceleration; local background curvature", "orbital;R8;cosmology_link", "negligible local bound or cosmology-calibrated constant row"),
        ("NEH4720_9_source_normalization", "delta_w, delta_kappa, epsilon_mu", "source-only prefactor or extra mass-channel coefficient", "WEP/R10/PPN/Gdot/source charge residual", "R1;R3;R4;R9;R10;R11", "4717 signature signed or finite source/test coefficient kernels"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "operator_id": operator_id,
            "coefficient_symbol": coeff,
            "operator_form": form,
            "weak_field_signature": signature,
            "affected_rows": affected,
            "zero_or_bound_requirement": requirement,
            "status": "retained_until_parent_zero_or_source_bound",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for operator_id, coeff, form, signature, affected, requirement in rows
    ]


def projection_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("PROJ4720_0_Poisson", "Delta_Poisson", "sum_i Pi_N_i c_i <= PB4719_1_fractional_density_region target", "E00/non-EH source component and same-source normalization"),
        ("PROJ4720_1_gamma", "gamma_minus_1", "sum_i Pi_gamma_i c_i <= gamma_bound", "spatial tracefree/non-EH slip map"),
        ("PROJ4720_2_beta", "beta_minus_1", "sum_i Pi_beta_i c_i <= beta_bound", "2PN nonlinear/source-normalized map"),
        ("PROJ4720_3_preferred_frame", "alpha1_alpha2_alpha3_xi", "sum_i Pi_vec_i c_i <= row-specific alpha/xi bounds", "vector/torsion/boundary/domain maps"),
        ("PROJ4720_4_R10", "alpha_lambda", "alpha_predicted(lambda;c_i,m_i) <= alpha_bound(lambda) for all lambda rows", "range/mass/coupling map; no anchor-only pass"),
        ("PROJ4720_5_Gdot_orbital_clock", "Gdot_clock_orbital", "D_tau ln(lambda_D/M_EH^2)+sum_i Pi_time_i c_i below local drift bounds", "stationarity/readout/tau-map"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "projection_id": projection_id,
            "observable": observable,
            "projection_contract": contract,
            "required_inputs": required,
            "status": "kernel_shape_only_needs_numeric_source_rows",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for projection_id, observable, contract, required in rows
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    gates = [
        ("GATE4720_0_selector_signed", "All EH selector clauses are signed by the parent action.", "PARENT_EH_SELECTOR_UNSIGNED"),
        ("GATE4720_1_no_extra_operator_targets", "No extra scalar/vector/tensor/torsion/memory/source coefficient target remains in the local collar.", "NONEH_OPERATOR_TARGET_AUDIT_NEEDED"),
        ("GATE4720_2_matrix_numeric_or_zero", "Every retained non-EH row has theorem-zero or numeric coefficient with units/source path.", "NONEH_MATRIX_UNFILLED"),
        ("GATE4720_3_projection_kernels_sourced", "Pi_N/Pi_PPN/Pi_R10/Pi_clock/Pi_orbital kernels are numeric and source-backed.", "PROJECTION_KERNELS_SYMBOLIC"),
        ("GATE4720_4_no_poisson_to_ppn_shortcut", "Poisson, gamma, beta, preferred-frame, conservation and Gdot rows use one shared convention.", "FULL_PPN_SHARED_CONVENTION_NEEDED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "requirement": requirement,
            "passed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, requirement, blocker in gates
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4720_0_no_EH_claim",
            "rule": "Do not claim the MTS parent has derived EH unless every selector clause is signed in the parent object language.",
            "reason": "4720 supplies a conditional theorem plus matrix fallback, not a global parent proof.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4720_1_no_symbolic_matrix_pass",
            "rule": "Symbolic non-EH rows cannot pass R10/PPN/orbital/clock tests.",
            "reason": "Each retained coefficient needs theorem-zero or numeric source-backed rows.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4720_0",
            "decision": DECISION,
            "meaning": "The local left-hand problem is now a sharp selector fork: under the standard single-geometry two-derivative covariant IR signature, EH is forced; every violation is a named coefficient in a matrix that can feed local tests.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4720_0",
            "status": "private_nonclaim_EH_selector_or_matrix_checkpoint",
            "summary": "Conditional EH selector theorem written, parent signature clauses staged, non-EH operator coefficient matrix and projection kernels created.",
            "claim_allowed": False,
            "timestamp_utc": ts,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4720_0",
            "next_target": NEXT_TARGET,
            "why": "The least-scrutinized route is to prove the two-derivative EH selector; the fallback with biggest empirical bite is the R2/f(R) scalar finite-range row.",
            "derive_first": "prove or reject the parent two-derivative EH selector clause with explicit exclusion of R2/f(R), Ricci/Weyl2, torsion, scalar, vector, disformal and memory slots",
            "fallback": "fill the R2/f(R) scalar row with mass/range/coupling normalization and R10/gamma/beta projection contracts",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def write_docs(
    ts: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    source_lines = "\n".join(
        f"- `{r['source_id']}`: `{r['source_path']}`; exists={r['exists']}; needle_found={r['needle_found']}; role={r['role']}"
        for r in sources
    )
    theorem_lines = "\n".join(f"- `{r['row_id']}` ({r['status']}): {r['claim']}" for r in theorem)
    clause_lines = "\n".join(f"- `{r['clause_id']}`: {r['clause']} Blocks `{r['blocks']}`; fallback `{r['fallback_coefficient']}`." for r in clauses)
    matrix_lines = "\n".join(f"- `{r['operator_id']}` / `{r['coefficient_symbol']}`: {r['operator_form']} -> {r['weak_field_signature']}" for r in matrix)
    projection_lines = "\n".join(f"- `{r['projection_id']}` / `{r['observable']}`: {r['projection_contract']}" for r in projections)
    gate_lines = "\n".join(f"- `{r['gate_id']}`: passed={r['passed']}; blocker=`{r['blocker']}`." for r in gates)

    write_text(
        DOC_PATH,
        f"""# 4720 - EH Reduction Parent Signature or Non-EH Operator Coefficient Matrix

Generated: `{ts}`

## Purpose

4719 derived the weak-field bridge:

`nabla^2 Phi_N = 4*pi*G_eff*rho + (c^2/2)E_00`.

So the next highest-leverage question is whether `E_mu_nu` is actually zero at the local principal GR order. This checkpoint takes the least hand-wavy route:

- try to force EH from a parent IR selector;
- if the selector is not signed, every failure becomes a coefficient in a non-EH operator matrix.

## Selector Theorem

If the visible local geometry is single-metric/coframe, local, covariant, parity-even and two-derivative, with algebraic/silent torsion and no extra scalar/vector/disformal/memory/source coefficient target, the EH/EC bulk term is the unique principal operator up to `Lambda`, topological and boundary terms.

This is the cleanest route because it does not tune local tests. It narrows the theory language until the GR left-hand side is forced.

## Theorem Rows

{theorem_lines}

## Parent Signature Clauses

{clause_lines}

## Non-EH Coefficient Matrix

{matrix_lines}

## Projection Kernels

{projection_lines}

## Gates

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
        f"""# PPC4161 4720 - EH Reduction Parent Signature or Non-EH Operator Matrix

Generated: `{ts}`

## Formal Fork

Let the local visible geometry sector satisfy:

single observed coframe/metric + local covariant 4-form + parity-even two-derivative IR order + algebraic torsion/nonmetricity silence + no extra scalar/vector/disformal/memory/source coefficient targets.

Then the principal bulk action is:

`S_geo,IR = (M_EH^2/2) int sqrt(-g) R - int sqrt(-g) Lambda + S_top + S_boundary`

and therefore the 4719 `E_mu_nu` residual has no principal local bulk source.

If any clause fails, the failure is represented by the coefficient matrix in `{OPERATOR_MATRIX_CSV}` and projected through `{PROJECTION_CSV}`.

## Nonclaim Boundary

The theorem is conditional until the parent action signs the selector. Matrix rows are not empirical evidence until coefficients, units, source paths and projection kernels are filled or theorem-zeroed.

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
        "claim": "4720 states the conditional EH selector theorem and stages a non-EH operator coefficient matrix for every selector failure.",
        "current_evidence": "Generated source register, EH selector theorem rows, parent signature clauses, non-EH operator coefficient matrix, projection kernels, gates, firewalls, decision, status, next target and validation.",
        "status": "conditional_EH_selector_or_nonEH_matrix_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating the EH selector theorem as parent-signed before the parent object language excludes every non-EH coefficient target.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "EH reduction parent signature or non-EH operator coefficient matrix",
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

`4720-Y5-R2FR-EH-reduction-parent-signature-or-nonEH-operator-coefficient-matrix.md`

## Decision

`{DECISION}`

## What moved forward

- The local GR left-hand problem is now a sharp fork, not a vague gap.
- If the parent signs the single-geometry/local/covariant/parity-even/two-derivative selector, EH is forced up to `Lambda`, topological and boundary terms.
- If any selector clause fails, the failure is routed into a named non-EH coefficient matrix.
- No EH/local-GR/R10/PPN claim fires until either the selector is signed or the matrix is filled and bounded.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def validation_rows(
    ts: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4720_sources_exist", all(r["exists"] for r in sources), "all cited local source paths exist"),
        ("VAL4720_needles_found", all(r["needle_found"] for r in sources), "all cited source needles found"),
        ("VAL4720_selector_theorem", any(r["row_id"] == "EHS4720_0_selector_theorem" for r in theorem), "EH selector theorem row present"),
        ("VAL4720_signature_clauses", len(clauses) >= 8 and any(r["clause_id"] == "EHSC4720_2_two_derivative_IR" for r in clauses), "signature clauses present"),
        ("VAL4720_operator_matrix", len(matrix) >= 10 and any(r["operator_id"] == "NEH4720_0_R2_fR_scalar" for r in matrix), "non-EH operator matrix present"),
        ("VAL4720_projection_kernels", len(projections) >= 6 and any(r["projection_id"] == "PROJ4720_4_R10" for r in projections), "projection kernels present"),
        ("VAL4720_gates_not_passing", not all(bool(r["passed"]) for r in gates), "promotion gates not all passing"),
        ("VAL4720_no_claim_allowed", all(not bool(r.get("valid_for_claim")) for r in sources + theorem + clauses + matrix + projections + gates), "no row allows a claim"),
        ("VAL4720_doc_written", DOC_PATH.exists() and DOC_PATH.stat().st_size > 1000, "checkpoint document written"),
        ("VAL4720_formal_written", FORMAL_PATH.exists() and FORMAL_PATH.stat().st_size > 500, "formal packet document written"),
        ("VAL4720_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
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
            "validation_id": "VAL4720_OVERALL",
            "passed": overall,
            "detail": "4720 artifacts validate as private nonclaim EH selector/matrix checkpoint",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()

    sources = source_register(ts)
    theorem = selector_theorem_rows(ts)
    clauses = signature_clause_rows(ts)
    matrix = operator_matrix_rows(ts)
    projections = projection_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(SELECTOR_THEOREM_CSV, theorem)
    write_csv(SIGNATURE_CLAUSES_CSV, clauses)
    write_csv(OPERATOR_MATRIX_CSV, matrix)
    write_csv(PROJECTION_CSV, projections)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    write_docs(ts, sources, theorem, clauses, matrix, projections, gates)
    update_claims(ts)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: EH is now a conditional selector theorem; every selector failure is routed into a named non-EH coefficient matrix.
- Still blocked: parent signature has not signed the selector; matrix rows are symbolic until theorem-zero or numeric source-backed coefficients exist.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts the 4719 `E_mu_nu` residual into either an EH selector proof target or an explicit non-EH operator matrix.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    update_resume(ts)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    write_csv(VALIDATION_CSV, validation_rows(ts, sources, theorem, clauses, matrix, projections, gates))


if __name__ == "__main__":
    main()
