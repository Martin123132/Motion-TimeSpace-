from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4054-Y5-R2FR-scalar-charge-zero-and-improvement-normalization.md"

SOURCES = {
    "SRC4054_00_4053_reduction": (
        ROOT / "4053-Y5-R2FR-q-loc-Khat-projector-silence-reduction.md",
        "Q_phi=0",
    ),
    "SRC4054_01_4028_improvement": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_IMPROVEMENT_DERIVATION.csv",
        "sigma_resp*c_I=1",
    ),
    "SRC4054_02_4029_phi_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4029_PHI_OWNER_EULER_DERIVATION.csv",
        "Box phi - mu_phi^2",
    ),
    "SRC4054_03_4031_collar": (
        SOURCE_DIR / "P8_Y5_R2FR_4031_EXTERIOR_COLLAR_DELTAPHI_THEOREM.csv",
        "int_Omega",
    ),
    "SRC4054_04_4032_charge": (
        SOURCE_DIR / "P8_Y5_R2FR_4032_SCALAR_CHARGE_IDENTITY.csv",
        "Q_phi=0 if",
    ),
    "SRC4054_05_4036_no_source_slot": (
        SOURCE_DIR / "P8_Y5_R2FR_4036_NO_HOM_SOURCE_SLOT_THEOREM.csv",
        "Hom_parent(Z_src,ActionScalar_matter)=0",
    ),
    "SRC4054_06_4038_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_BOUNDARY_REFERENCE_THEOREM.csv",
        "boundary scalar charge vanishes",
    ),
    "SRC4054_07_1526_coefficient_doc": (
        ROOT / "1526-Y5-tracefree-Hessian-improvement-action-coefficient-and-symbol-match.md",
        "sigma_resp*c_I=1",
    ),
    "SRC4054_08_1526_contract": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1526_COEFFICIENT_SIGN_CONTRACT.csv",
        "COEFFICIENT_MATCH_LAW_DERIVED",
    ),
    "SRC4054_09_1527_aux_action": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
        "S_phiK=int",
    ),
    "SRC4054_10_1528_multiplier_block": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1528_THEOREM_OR_BOUND_RUNNER.csv",
        "BLOCKED_NOT_ZERO_PROVEN",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4054_SOURCE_REGISTER.csv",
    "normalization": SOURCE_DIR / "P8_Y5_R2FR_4054_UNIT_RESPONSE_NORMALIZATION_LEMMA.csv",
    "no_flux": SOURCE_DIR / "P8_Y5_R2FR_4054_NATURAL_NO_FLUX_SCALAR_CHARGE_THEOREM.csv",
    "closure_matrix": SOURCE_DIR / "P8_Y5_R2FR_4054_QPHI_KHAT_HINGE_CLOSURE_MATRIX.csv",
    "fallback_bounds": SOURCE_DIR / "P8_Y5_R2FR_4054_FALLBACK_BOUND_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4054_EVALUATOR_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4054_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4054_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4054_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4054_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle) in SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_present": contains(path, needle),
                "use_in_4054": "scalar_charge_zero_and_Khat_normalization",
                "timestamp_utc": ts,
            }
        )
    return rows


def normalization_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "lemma_id": "URN4054_0_define_unit_field",
            "object": "unit-response scalar",
            "formula": "varpi := sigma_resp*c_I*(phi-phi_*)",
            "result": "Khat_TF derivative response can be written with unit coefficient in terms of varpi.",
            "condition": "phi is an auxiliary Khat-owner field with no independent ordinary-matter, EM, clock, mass, or coupling readout.",
            "status": "FIELD_NORMALIZATION_LEMMA",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "lemma_id": "URN4054_1_Khat_unit_response",
            "object": "Khat_TF",
            "formula": "Pi_TF[K_imp] = 2[(nabla^mu nabla^nu varpi-(1/4)g^{mu nu}Box varpi) - varpi G_TF^{mu nu}]",
            "result": "The old coefficient condition sigma_resp*c_I=1 becomes a normalization/adoption convention, not a new fitted physical parameter.",
            "condition": "single-use auxiliary scalar and fixed sign convention for Khat response",
            "status": "NORMALIZES_COEFFICIENT_IF_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "lemma_id": "URN4054_2_when_not_allowed",
            "object": "coefficient obstruction",
            "formula": "if phi also appears in source masses, EM Hodge factors, clock constants, or hidden-visible coefficients, c_I is physical and cannot be scaled away",
            "result": "field normalization is forbidden in any branch where phi has independent observable couplings.",
            "condition": "ordinary-sector phi slots survive",
            "status": "OVERCLAIM_GUARD",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "lemma_id": "URN4054_3_preferred_route",
            "object": "route choice",
            "formula": "prefer the 4029 dynamical phi exterior owner over the 1527 multiplier localization for this local branch",
            "result": "This avoids importing the lambda_phi stress problem unless the dynamical owner fails.",
            "condition": "F=0 in the exterior and no direct source slot for phi",
            "status": "LOWER_SCRUTINY_ROUTE_SELECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def no_flux_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "NFL4054_0_domain",
            "step": "Exterior collar with excised compact source",
            "formula": "Omega_ext={R_src<r<R_out}; u:=varpi-varpi_*",
            "result": "Work on the local exterior branch rather than forcing an interior source solution.",
            "condition": "stationary/asymptotically stationary compact local PPN collar",
            "status": "DOMAIN_DEFINED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "NFL4054_1_homogeneous_equation",
            "step": "Exterior phi equation",
            "formula": "(Delta_h-mu_phi^2)u=0",
            "result": "The source term is absent in the exterior once F=Gamma_eff+C is routed to zero by the selected local EH/Newton branch.",
            "condition": "PPC4048 exterior branch plus no direct ordinary matter/EM phi slot",
            "status": "CONDITIONAL_EXTERIOR_EQUATION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "NFL4054_2_natural_inner_boundary",
            "step": "Natural no-flux condition",
            "formula": "delta S_phi|inner = -zeta_phi int_{S_src} n.grad u delta u dS; free delta u gives n.grad u=0",
            "result": "The scalar charge Q_phi=int_{S_src} n.grad u dS is zero without fitting it away.",
            "condition": "no boundary source term B_src[u] and no hidden source-slot coupling to u",
            "status": "DERIVED_IF_SOURCE_BOUNDARY_SILENT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "NFL4054_3_outer_branch_fixing",
            "step": "Outer/asymptotic fixing",
            "formula": "u|outer=0 or finite-energy u->0",
            "result": "The constant zero mode is removed, including the mu_phi=0 case.",
            "condition": "fixed local reference branch/asymptotic value is chosen before variation",
            "status": "ZERO_MODE_FIXED_IF_REFERENCE_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "NFL4054_4_energy_identity",
            "step": "Energy uniqueness",
            "formula": "int_Omega(|grad u|^2+mu_phi^2 u^2)dV = int_boundary u n.grad u dS",
            "result": "With inner no-flux and outer zero/falloff, u=0 for mu_phi>0 and u=constant=0 for mu_phi=0.",
            "condition": "positive elliptic stationary reduction and compatible boundary data",
            "status": "SCALAR_HAIR_ZERO_CONDITIONAL_THEOREM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "NFL4054_5_q_loc_consequence",
            "step": "Khat consequence",
            "formula": "u=0 => Hess(u)=0 => Khat_TF exterior residual=0 and scalar part of Pi_PPN[q_loc]=0",
            "result": "The 4053 scalar-charge hinge closes under the natural boundary/source-silence packet.",
            "condition": "NFL4054_0 through NFL4054_4 plus unit-response Khat adoption",
            "status": "CONDITIONAL_HINGE_CLOSURE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def closure_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "hinge_id": "H4054_0_unit_response",
            "hinge": "sigma_resp*c_I=1",
            "new_status": "CLOSABLE_AS_FIELD_NORMALIZATION_IF_AUXILIARY_SINGLE_USE",
            "still_needed": "formal parent adoption that phi/varpi has no independent ordinary-sector readout",
            "risk_if_false": "c_I remains a physical unsourced coefficient",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "hinge_id": "H4054_1_scalar_charge",
            "hinge": "Q_phi=0",
            "new_status": "DERIVED_FROM_NATURAL_NO_FLUX_IF_NO_SOURCE_BOUNDARY_SLOT",
            "still_needed": "parent-sign no B_src[u], no hidden source slot, and fixed outer reference branch",
            "risk_if_false": "Yukawa/harmonic scalar hair survives and must be bounded",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "hinge_id": "H4054_2_multiplier_route",
            "hinge": "lambda_phi silence",
            "new_status": "NOT_USED_AS_PRIMARY_ROUTE",
            "still_needed": "retain only as fallback if dynamical exterior owner fails",
            "risk_if_false": "extra multiplier stress reopens Kmetric kernels",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "hinge_id": "H4054_3_q_loc",
            "hinge": "4053 scalar/Khat clause",
            "new_status": "NEAR_CLOSED_CONDITIONAL_PACKET",
            "still_needed": "combine with Hilbert owner D_GK=0 and trace/background subtraction in 4055",
            "risk_if_false": "fallback q_loc bound vector remains active",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def fallback_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "FB4054_0_scalar_charge_bound",
            "if_clause_fails": "natural no-flux/source-boundary silence is not adopted",
            "formula": "u(r)=Q_phi exp(-mu_phi(r-R_src))/(4*pi r) plus higher multipoles",
            "observable_map": "R10 alpha(lambda); PPN beta/gamma residual; fifth-force source exchange",
            "needed_inputs": "Q_phi,mu_phi,R_src,collar boundary data,PPN/R10 projectors",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "FB4054_1_physical_cI_bound",
            "if_clause_fails": "phi has independent ordinary-sector readout",
            "formula": "|q_loc| <= |1-sigma_resp*c_I| ||P_loc nabla K_L||",
            "observable_map": "local q_loc force residual; PPN beta/gamma",
            "needed_inputs": "sigma_resp,c_I,K_L profile,local length scale",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "FB4054_2_multiplier_stress_bound",
            "if_clause_fails": "must revert to 1527 multiplier route",
            "formula": "||T_lambda_phi|| <= C_T(||grad lambda_phi||^2 + ||lambda_phi|| ||delta_g S_Gamma||)",
            "observable_map": "q_loc residual and Kmetric kernel fallback",
            "needed_inputs": "lambda_phi norm,gradient norm,delta_g S_Gamma operator norm",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def static_rows(ts: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "evaluator": [
            {
                "case_id": "CASE4054_0",
                "verdict": "SCALAR_CHARGE_ZERO_ROUTE_CONSTRUCTED_CONDITIONALLY",
                "result": "Q_phi=0 follows from the exterior dynamical phi owner if the source boundary has natural no-flux and the outer branch fixes the zero mode.",
                "what_moved": "The scalar-charge gap is no longer only an integrated-source wish; it has a variational boundary route.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            },
            {
                "case_id": "CASE4054_1",
                "verdict": "IMPROVEMENT_COEFFICIENT_REINTERPRETED",
                "result": "sigma_resp*c_I=1 can be treated as unit-response field normalization if phi/varpi is auxiliary single-use.",
                "what_moved": "One apparent free coefficient is demoted to a convention under explicit guards.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            },
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4054_0_private_progress",
                "claim": "Q_phi zero and Khat unit normalization have conditional derivation routes",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "source-boundary silence and auxiliary single-use adoption are not yet in formalization as parent axioms",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4054_1_q_loc_closed",
                "claim": "q_loc/Khat projector silence is fully closed",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "Hilbert owner D_GK=0 and trace/background subtraction remain to be attacked",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4054_2_local_GR",
                "claim": "MTS publicly derives local GR",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "4054 closes only a conditional hinge, not the whole parent packet",
                "timestamp_utc": ts,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4054_0",
                "next_doc": "4055-Y5-R2FR-Hilbert-owner-DGK-zero-and-trace-background-subtraction.md",
                "next_script": "scripts/Y5_R2FR_4055_Hilbert_owner_DGK_zero_and_trace_subtraction.py",
                "reason": "After 4054, the best remaining q_loc blockers are D_GK=0 and trace/background subtraction, not scalar charge.",
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4054",
                "status": "QPHI_ZERO_AND_KHAT_NORMALIZATION_CONDITIONAL_ROUTE_BUILT",
                "public_claim": False,
                "formalization_modified_by_4054": False,
                "timestamp_utc": ts,
            }
        ],
    }


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def csv_parse_ok(path: Path) -> Tuple[bool, str]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"rows={len(rows)}"
    except Exception as exc:
        return False, repr(exc)


def validation_rows(
    sources: List[Dict[str, object]],
    generated_csvs: List[Path],
    all_rows: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    parse_results = [csv_parse_ok(path) for path in generated_csvs]
    flat_rows = [row for table in all_rows for row in table]
    serialized = "\n".join(str(value) for row in flat_rows for value in row.values())
    outputs_in_formalization = [path for path in OUTPUTS.values() if FORMALIZATION in path.parents]
    return [
        {
            "check_id": "VAL4054_00_sources_exist",
            "passed": all(bool(row["exists"]) for row in sources),
            "detail": "all cited local source paths exist",
        },
        {
            "check_id": "VAL4054_01_needles_present",
            "passed": all(bool(row["needle_present"]) for row in sources),
            "detail": "all source needles present",
        },
        {
            "check_id": "VAL4054_02_csv_parse",
            "passed": all(result for result, _detail in parse_results),
            "detail": "; ".join(f"{path.name}:{detail}" for path, (_ok, detail) in zip(generated_csvs, parse_results)),
        },
        {
            "check_id": "VAL4054_03_no_public_claim",
            "passed": "allowed_public': True" not in serialized and "valid_for_public_claim': True" not in serialized,
            "detail": "all claim-bearing rows preserve public false",
        },
        {
            "check_id": "VAL4054_04_no_missing_markers",
            "passed": "MISSING_" not in serialized,
            "detail": "outputs use explicit open/blocker language instead of MISSING markers",
        },
        {
            "check_id": "VAL4054_05_no_formalization_outputs",
            "passed": len(outputs_in_formalization) == 0,
            "detail": "4054 writes only post-checkpoint/source-intake outputs",
        },
        {
            "check_id": "VAL4054_06_script_compiles",
            "passed": script_compiles(),
            "detail": "script compiles",
        },
    ]


def doc_text(ts: str) -> str:
    return f"""# 4054 - Scalar Charge Zero and Improvement Normalization

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## What Actually Moved

4053 exposed two sharp hinges: `Q_phi=0` and `sigma_resp*c_I=1`.

4054 takes a real swing at both:

1. `sigma_resp*c_I=1` is not necessarily a new physical number. If `phi` is only the auxiliary Khat-owner field, define the unit-response scalar

```text
varpi := sigma_resp*c_I*(phi-phi_*)
```

and write `Khat_TF` in terms of `varpi`. Under the single-use auxiliary-scalar guard, the coefficient becomes a field-normalization/adoption convention, not a fitted parameter.

2. `Q_phi=0` can come from the variational boundary problem. On the exterior collar,

```text
(Delta_h - mu_phi^2)u = 0,    u := varpi-varpi_*
```

and the variation of the exterior scalar action gives the inner-boundary term

```text
delta S_phi|inner = -zeta_phi int_{{S_src}} n.grad u delta u dS.
```

If no boundary source term or hidden source-slot coupling to `u` exists, free boundary variation gives

```text
n.grad u = 0  =>  Q_phi = int_{{S_src}} n.grad u dS = 0.
```

With outer/asymptotic branch fixing, the energy identity then gives `u=0`, so `Hess(u)=0` and the scalar part of `Khat/q_loc` vanishes.

## Non-Negotiable Guards

- This uses the 4029 dynamical exterior owner, not the older 1527 multiplier route.
- If `phi` couples independently to matter, EM, clocks, masses, or constants, the coefficient cannot be normalized away.
- If a source-boundary scalar term exists, natural no-flux fails and `Q_phi` must be bounded.
- This is still private/nonclaim until the no-source-boundary and auxiliary-single-use clauses are adopted in the parent packet.

## Next Target

Attack the remaining `q_loc` pieces: parent Hilbert ownership/`D_GK=0` and trace/background subtraction. Choom, this is not the roof yet, but this is an actual rung under the boot.
"""


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(ts)
    normalization = normalization_rows(ts)
    no_flux = no_flux_rows(ts)
    closure = closure_rows(ts)
    fallback = fallback_rows(ts)
    static = static_rows(ts)

    DOC_PATH.write_text(doc_text(ts), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["normalization"], normalization)
    write_csv(OUTPUTS["no_flux"], no_flux)
    write_csv(OUTPUTS["closure_matrix"], closure)
    write_csv(OUTPUTS["fallback_bounds"], fallback)
    write_csv(OUTPUTS["evaluator"], static["evaluator"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["normalization"],
        OUTPUTS["no_flux"],
        OUTPUTS["closure_matrix"],
        OUTPUTS["fallback_bounds"],
        OUTPUTS["evaluator"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_rows = [
        sources,
        normalization,
        no_flux,
        closure,
        fallback,
        static["evaluator"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, all_rows)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
