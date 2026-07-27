from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4061-Y5-R2FR-connection-domain-boundary-kernels-zero-or-bound.md"

DECISION = "CONNECTION_DOMAIN_BOUNDARY_KERNELS_ZERO_IN_SELECTED_PARENT_BRANCH_FALLBACK_BOUNDS_ACTIVE"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4061_00_4059_queue": (
        SOURCE_DIR / "P8_Y5_R2FR_4059_DELTAK_COMPONENT_QUEUE.csv",
        "DKC4059_3_connection",
        "4059 identifies connection, domain, and boundary kernels as the remaining Delta_K queue.",
    ),
    "SRC4061_01_4060_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4060_NEXT_TARGET.csv",
        "connection, domain/projector, and boundary/reference response terms",
        "4060 selects this checkpoint after killing the m/L_cg first variation.",
    ),
    "SRC4061_02_4056_packet": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
        "source-blind boundary/reference, q-basic projector/domain",
        "4056 local packet already contains the side-channel ownership clauses.",
    ),
    "SRC4061_03_4055_hilbert": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_HILBERT_RESPONSE_DEFINITION.csv",
        "T_Hilbert_GK",
        "4055 makes the GK response a Hilbert-stress object rather than a free Khat residual.",
    ),
    "SRC4061_04_4043_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv",
        "PZS4043_0_selected_signature",
        "4043 supplies the selected projector/domain zero theorem.",
    ),
    "SRC4061_05_4043_factor": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_PROJECTOR_STRESS_FACTORIZATION.csv",
        "PSF4043_0_projector_metric_variation",
        "4043 factorizes projector/domain stress pieces and their fallback terms.",
    ),
    "SRC4061_06_4038_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_BOUNDARY_REFERENCE_THEOREM.csv",
        "BND4038_0_boundary_action",
        "4038 gives the source-blind boundary/reference owner.",
    ),
    "SRC4061_07_4038_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "PNT4038_1_exterior_collar",
        "4038 keeps local stationary Poynting flux from becoming an extra source term.",
    ),
    "SRC4061_08_3911_connection": (
        SOURCE_DIR / "P8_Y5_R2FR_3911_SOURCE_DOMAIN_CONNECTION_DERIVATION.csv",
        "CON3911_2_commutator_identity",
        "3911 derives the source-domain connection commutator identity.",
    ),
    "SRC4061_09_3912_massflat": (
        SOURCE_DIR / "P8_Y5_R2FR_3912_MASS_FLAT_CONNECTION_BRANCH_GATE.csv",
        "MF3912_0_connection_coefficients",
        "3912 gives the mass-flat source-silent connection branch.",
    ),
    "SRC4061_10_3846_nonlc": (
        SOURCE_DIR / "P8_Y5_R2FR_3846_CONNECTION_READOUT_RESIDUALS.csv",
        "B_nonLC",
        "3846 records the non-Levi-Civita fallback residual.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4061_SOURCE_REGISTER.csv",
    "kernel_decomposition": SOURCE_DIR / "P8_Y5_R2FR_4061_KERNEL_DECOMPOSITION.csv",
    "connection_theorem": SOURCE_DIR / "P8_Y5_R2FR_4061_CONNECTION_KERNEL_THEOREM.csv",
    "domain_theorem": SOURCE_DIR / "P8_Y5_R2FR_4061_DOMAIN_PROJECTOR_KERNEL_THEOREM.csv",
    "boundary_theorem": SOURCE_DIR / "P8_Y5_R2FR_4061_BOUNDARY_REFERENCE_KERNEL_THEOREM.csv",
    "fallback_bounds": SOURCE_DIR / "P8_Y5_R2FR_4061_FALLBACK_BOUND_VECTOR.csv",
    "decision": SOURCE_DIR / "P8_Y5_R2FR_4061_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4061_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4061_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4061_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4061_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def kernel_decomposition_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "kernel_id": "CDB4061_0_sum",
            "object": "Delta_K_CDB",
            "formula": "Delta_K_CDB := K_conn + K_domain + K_boundary",
            "meaning": "the remaining first-order technical Delta_K residue after 4060 chain silence",
            "selected_branch_result": "sum is zero if all three ownership theorems below are parent-adopted",
            "fallback": "absolute no-cancellation bound over the three kernels",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "kernel_id": "CDB4061_1_connection",
            "object": "K_conn",
            "formula": "connection response from Christoffel/Hodge/covariant-derivative metric variation",
            "meaning": "dangerous only if the connection is independent, non-LC, source-active, or not included in the Hilbert variation",
            "selected_branch_result": "not an independent kernel when nabla=nabla[g_obs] and all derivative terms live in the parent action",
            "fallback": "B_nonLC plus source-domain connection derivative envelope",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "kernel_id": "CDB4061_2_domain",
            "object": "K_domain",
            "formula": "domain/projector/support response from P_D, D_loc, collar, and selector stress",
            "meaning": "dangerous only if support/projector/collar variables are dynamical metric-dependent objects",
            "selected_branch_result": "zero under q-basic fixed-domain/projector selected branch from 4043",
            "fallback": "projector metric-variation, domain-motion, constraint, wall, and denominator bound vector",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "kernel_id": "CDB4061_3_boundary",
            "object": "K_boundary",
            "formula": "boundary/reference/corner/Poynting response",
            "meaning": "dangerous only if boundary/reference data carry source/readout drift or nonstationary flux",
            "selected_branch_result": "zero under source-blind GHY/exact/topological boundary and fixed H_ref/no-flux local collar from 4038",
            "fallback": "flux, boundary charge, reference drift, and corner-term bound vector",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def connection_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "CONN4061_0_metric_owner",
            "statement": "The selected local parent branch uses the observed Levi-Civita connection nabla[g_obs], not an independent local connection field.",
            "condition": "local field list is Met_obs plus matter/EM/GK auxiliaries; torsion, nonmetricity, and shadow-frame connections are excluded from the local <=2PN packet",
            "derived_result": "Gamma_obs - LeviCivita[g_obs] = 0 as an independent local source slot",
            "status": "SELECTED_PARENT_BRANCH_CLAUSE",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "CONN4061_1_variation_owner",
            "statement": "Metric variation of Christoffel/Hodge/covariant derivative terms is already part of the Hilbert variation of the parent action.",
            "condition": "matter, EM, and GK derivative terms are varied before readout, with differentiability boundary terms fixed",
            "derived_result": "Palatini/Hilbert response terms are not a separate K_conn residual after T_Hilbert is formed",
            "status": "HILBERT_VARIATION_ABSORPTION",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "CONN4061_2_source_domain",
            "statement": "For source-silent vertical residuals, the source-domain connection is mass-flat.",
            "condition": "v_X in ker(Dq_src), source coordinates M_H_ref and sigma^a are q-basic, and reference/surface/frame variables are fixed before variation",
            "derived_result": "A_X^A = 0 and partial_M A_X^A = 0 for A in {M,a,I}; the 3911 commutator source-connection residual vanishes",
            "status": "SOURCE_SILENT_MASS_FLAT_IMPORT",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "CONN4061_3_result",
            "statement": "K_conn is zero in the selected parent branch as an independent first-order Delta_K kernel.",
            "condition": "CONN4061_0 through CONN4061_2 hold and are adopted before local tests/readout",
            "derived_result": "K_conn_parent = 0; if any clause fails, use the non-LC/source-connection fallback rows",
            "status": "CONNECTION_KERNEL_ZERO_SELECTED_BRANCH_ELSE_BOUND",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def domain_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "DOM4061_0_q_basic_projector",
            "statement": "The selected local projector/domain is a q-basic fixed readout/topological label, not a dynamical stress carrier.",
            "condition": "delta_g P_D = 0, D_D P_D = 0, fixed collar, and no post-readout source support fitting",
            "derived_result": "projector metric-variation and domain-motion kernels vanish",
            "status": "PROJECTOR_DOMAIN_OWNER_IMPORTED_FROM_4043",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "DOM4061_1_constraint_wall",
            "statement": "The selected compact collar has no active selector multiplier, wall flux, or STF wall stress.",
            "condition": "chi_local = 0, lambda_local = 0, Phi_D = 0, tau_wall_TF = 0, and the Hilbert denominator is the same source branch",
            "derived_result": "constraint, flux, anisotropy, and extra-denominator pieces vanish",
            "status": "DOMAIN_STRESS_FACTOR_ZERO_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "DOM4061_2_result",
            "statement": "K_domain is zero in the selected parent branch as an independent first-order Delta_K kernel.",
            "condition": "DOM4061_0 and DOM4061_1 hold and are adopted before variation/readout",
            "derived_result": "K_domain_parent = 0; if the selected signature is rejected, use the alpha/xi/domain fallback vector",
            "status": "DOMAIN_KERNEL_ZERO_SELECTED_BRANCH_ELSE_BOUND",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def boundary_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "BND4061_0_differentiability_owner",
            "statement": "Boundary terms are differentiability/reference terms of the action, not independent source labels.",
            "condition": "S_boundary = S_GHY[g_obs] + B_exact/topological - H_ref[fixed reference], with B_GK chosen consistently with S_GK",
            "derived_result": "derivative-of-delta-g pieces are cancelled or owned by the variational principle",
            "status": "BOUNDARY_OWNER_IMPORTED_FROM_4038_AND_4056",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "BND4061_1_reference_lock",
            "statement": "The selected local reference is fixed before variation and cannot be re-fit by source labels or residual readout.",
            "condition": "D_source H_ref = D_readout H_ref = 0, and the boundary/reference object is source-blind",
            "derived_result": "source-dependent reference drift is zero",
            "status": "REFERENCE_DRIFT_ZERO_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "BND4061_2_no_flux_collar",
            "statement": "Stationary isolated local collars do not add a separate Poynting or scalar boundary-charge source.",
            "condition": "no imposed incoming/background radiation, no current crossing the collar, fixed/asymptotic or no-flux scalar boundary data",
            "derived_result": "Phi_EM_rad = 0 and direct scalar boundary charge is zero for the selected local exterior",
            "status": "LOCAL_NO_FLUX_AND_BOUNDARY_CHARGE_ZERO",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "BND4061_3_result",
            "statement": "K_boundary is zero in the selected parent branch as an independent first-order Delta_K kernel.",
            "condition": "BND4061_0 through BND4061_2 hold and are adopted before readout",
            "derived_result": "K_boundary_parent = 0; if any clause fails, use flux/reference/corner fallback rows",
            "status": "BOUNDARY_KERNEL_ZERO_SELECTED_BRANCH_ELSE_BOUND",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def fallback_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "FB4061_0_connection_nonLC",
            "kernel": "K_conn",
            "used_if": "independent connection, torsion, nonmetricity, or shadow-frame connection survives",
            "bound_formula": "B_conn_nonLC <= C_LC ||Gamma_obs - LeviCivita[g_obs]||_local + C_T ||Torsion|| + C_Q ||Nonmetricity||",
            "needed_inputs": "local connection convention, torsion/nonmetricity norms, PPN projection weights",
            "status": "SCHEMA_READY_NUMERIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "FB4061_1_connection_source_domain",
            "kernel": "K_conn",
            "used_if": "source-silent vertical branch or q_src ownership is rejected",
            "bound_formula": "|R_PiM| <= K_M|partial_M A_X^M| + K_shape||partial_M A_X^a|| + K_ref||partial_M A_X^I||",
            "needed_inputs": "K_M, K_shape, K_ref, partial_M A_X^M, partial_M A_X^a, partial_M A_X^I",
            "status": "IMPORTED_3911_BOUND_NUMERIC_INPUTS_MISSING",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "FB4061_2_domain_projector",
            "kernel": "K_domain",
            "used_if": "q-basic fixed projector/domain signature is rejected",
            "bound_formula": "B_domain <= C_P||delta_g P_D|| + C_D||D_D P_D|| + C_chi|lambda_D delta_g Sigma_D| + C_wall|tau_wall_TF| + C_flux|Phi_D|",
            "needed_inputs": "projector metric derivative, support derivative, constraint multiplier, wall STF stress, domain flux",
            "status": "4043_FALLBACK_VECTOR_ACTIVE_IF_SIGNATURE_REJECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "FB4061_3_boundary_reference",
            "kernel": "K_boundary",
            "used_if": "source-blind fixed-reference boundary theorem or stationary no-flux collar is rejected",
            "bound_formula": "B_boundary <= |c_B B_source| + |c_Poynting Phi_EM_rad| + C_ref|D_source H_ref| + C_corner|corner_source|",
            "needed_inputs": "B_source, Phi_EM_rad, H_ref source derivative, corner/source profile, coefficient priors",
            "status": "4038_FALLBACK_VECTOR_ACTIVE_IF_BOUNDARY_REJECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "FB4061_4_master",
            "kernel": "Delta_K_CDB",
            "used_if": "any connection/domain/boundary zero theorem clause is unsigned",
            "bound_formula": "|Delta_K_CDB| <= B_conn_nonLC + B_conn_source + B_domain + B_boundary",
            "needed_inputs": "all fallback rows above with no cancellation assumptions",
            "status": "MASTER_NO_CANCELLATION_BOUND_ACTIVE_UNTIL_PARENT_ADOPTION",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "decision": [
            {
                "decision_id": "DEC4061_0",
                "decision": DECISION,
                "parent_branch_result": "K_conn=K_domain=K_boundary=0 as independent first-order kernels in the selected parent branch",
                "fallback_branch": "non-LC/source-connection/domain/projector/boundary bounds remain active if any ownership clause is rejected",
                "valid_for_public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4061_0",
                "claim": "connection/domain/boundary first-order Delta_K kernels are zero in the selected parent branch",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "requires final parent-packet adoption and does not yet close second-order, calibration, or public local-GR gates",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4061_1",
                "claim": "all legacy connection/domain/boundary rows are zero",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "legacy/nonselected branches still require fallback bounds",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4061_2",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "formal adoption, second-order remainder, Newton-G calibration, and empirical PPN/R10 checks remain",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4061_0",
                "next_doc": "4062-Y5-R2FR-second-order-remainder-and-cnorm-newtonG-calibration-gate.md",
                "next_script": "scripts/Y5_R2FR_4062_second_order_remainder_and_cnorm_newtonG_calibration_gate.py",
                "reason": "after first-order CDB kernels are zeroed in the selected parent branch, the next honest gate is quadratic remainder plus universal source-normalization/Newton-G calibration",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4061",
                "status": "FIRST_ORDER_CDB_KERNELS_ZERO_IN_SELECTED_PARENT_BRANCH_PUBLIC_CLAIM_BLOCKED",
                "local_GR_claim": False,
                "public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover - validation output path
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("valid_for_public_claim", "allowed_public", "public_claim", "local_GR_claim"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public false"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    compile_ok, compile_detail = validate_script_compile()
    formal_outputs = list(FORMALIZATION.rglob("*4061*")) if FORMALIZATION.exists() else []
    return [
        {"check_id": "VAL4061_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4061_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4061_02_no_public_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4061_03_decision",
            "passed": DECISION in str(row_groups),
            "detail": "decision records selected parent zero branch plus fallback bounds",
        },
        {
            "check_id": "VAL4061_04_three_kernel_results",
            "passed": all(marker in str(row_groups) for marker in ("K_conn_parent = 0", "K_domain_parent = 0", "K_boundary_parent = 0")),
            "detail": "connection, domain, and boundary selected-branch zero results are all present",
        },
        {
            "check_id": "VAL4061_05_fallback_master",
            "passed": "MASTER_NO_CANCELLATION_BOUND_ACTIVE_UNTIL_PARENT_ADOPTION" in str(row_groups),
            "detail": "fallback master no-cancellation bound is present",
        },
        {
            "check_id": "VAL4061_06_no_formalization_outputs",
            "passed": len(formal_outputs) == 0,
            "detail": "4061 writes only post-checkpoint/source-intake outputs" if not formal_outputs else str(formal_outputs),
        },
        {"check_id": "VAL4061_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4061 - Connection/Domain/Boundary Kernels Zero or Bound

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## Result

4061 takes the residue left after 4060:

```text
Delta_K_CDB := K_conn + K_domain + K_boundary.
```

In the selected 4056 parent branch, these are not independent first-order source kernels:

- `K_conn = 0` because the local connection is `LeviCivita[g_obs]`, derivative metric response is inside the Hilbert variation, and source-silent verticals are mass-flat.
- `K_domain = 0` because the selected projector/domain is q-basic/fixed/topological, with no dynamic `P_D`, no domain-motion stress, no active constraint multiplier, and no wall flux/STF stress.
- `K_boundary = 0` because the boundary/reference sector is source-blind GHY/exact/topological data with fixed `H_ref`, local no-flux collar conditions, and no scalar boundary charge.

So:

```text
K_conn_parent = K_domain_parent = K_boundary_parent = 0
```

for the selected parent branch only.

## Guard

This is not a public local-GR claim and it does not rewrite legacy branches. If any ownership clause is rejected, the fallback is:

```text
|Delta_K_CDB|
<= B_conn_nonLC + B_conn_source + B_domain + B_boundary.
```

No cancellation between fallback channels is allowed.

## What Moved

The first-order `Delta_K` problem is no longer just a fog bank. It has a clean fork:

1. adopt the selected parent packet and these three kernels are zero as independent first-order leaks;
2. reject any clause and the exact bound rows identify what numerical/source inputs are required.

## Next Target

The next honest gate is the second-order remainder plus the universal source-normalization/Newton-G calibration route. That is where local GR/Newton can either start becoming a real derived limit or stay as guarded closure.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    decomposition = kernel_decomposition_rows(current_timestamp)
    connection = connection_theorem_rows(current_timestamp)
    domain = domain_theorem_rows(current_timestamp)
    boundary = boundary_theorem_rows(current_timestamp)
    fallback = fallback_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["kernel_decomposition"], decomposition)
    write_csv(OUTPUTS["connection_theorem"], connection)
    write_csv(OUTPUTS["domain_theorem"], domain)
    write_csv(OUTPUTS["boundary_theorem"], boundary)
    write_csv(OUTPUTS["fallback_bounds"], fallback)
    write_csv(OUTPUTS["decision"], static["decision"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["kernel_decomposition"],
        OUTPUTS["connection_theorem"],
        OUTPUTS["domain_theorem"],
        OUTPUTS["boundary_theorem"],
        OUTPUTS["fallback_bounds"],
        OUTPUTS["decision"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_row_groups = [
        sources,
        decomposition,
        connection,
        domain,
        boundary,
        fallback,
        static["decision"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, all_row_groups)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
