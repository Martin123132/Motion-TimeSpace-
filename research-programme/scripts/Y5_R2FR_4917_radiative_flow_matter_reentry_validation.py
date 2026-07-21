from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4917_radiative_flow_matter_reentry as research


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "mts_residuals"
TIMESTAMP = datetime.now(timezone.utc).isoformat()
MARKER = research.MARKER
NEXT_TARGET = research.NEXT_TARGET
CLAIM_STATUS = (
    "universal_nonlocal_EH_cross_channel_and_first_local_gravity_mediated_"
    "stress_contact_flow_trace_coefficients_derived_conditional_cone_product_"
    "bound_numeric_parent_matching_and_full_1PI_basis_open_private_nonclaim"
)
VARIABLES = (
    "UniversalCrossChannel4917_MTS",
    "StressContactBasis4917_MTS",
    "FlowMetricShift4917_MTS",
    "TraceMetricShift4917_MTS",
    "FlowZeroCriterion4917_MTS",
    "OverlapSupportGate4917_MTS",
    "ConeProductBound4917_MTS",
    "ScalarLoopAnchor4917_MTS",
    "WeylCoefficientOwnership4917_MTS",
    "RadiativeReentryGate4917_MTS",
)
EVIDENCE = (
    "P8_Y5_R2FR_4917_CHANNEL_DECOMPOSITION.csv",
    "P8_Y5_R2FR_4917_STRESS_CONTACT_BASIS.csv",
    "P8_Y5_R2FR_4917_PERFECT_FLUID_PROJECTION.csv",
    "P8_Y5_R2FR_4917_STATE_ZERO_CONDITIONS.csv",
    "P8_Y5_R2FR_4917_CONE_PRODUCT_BOUND.csv",
    "P8_Y5_R2FR_4917_COEFFICIENT_OWNERSHIP.csv",
    "P8_Y5_R2FR_4917_GATE_DECISION.csv",
    "P8_Y5_R2FR_4917_SOURCE_REGISTER.csv",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: str) -> bool:
    return value.strip().lower() == "true"


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError, UnicodeError):
        return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4916_VALIDATION.csv")
    channels = read_csv(OUTPUT / EVIDENCE[0])
    contacts = read_csv(OUTPUT / EVIDENCE[1])
    projections = read_csv(OUTPUT / EVIDENCE[2])
    zeros = read_csv(OUTPUT / EVIDENCE[3])
    bounds = read_csv(OUTPUT / EVIDENCE[4])
    ownership = read_csv(OUTPUT / EVIDENCE[5])
    decisions = read_csv(OUTPUT / EVIDENCE[6])
    sources = read_csv(OUTPUT / EVIDENCE[7])
    channel_map = {row["channel_id"]: row for row in channels}
    contact_map = {row["basis_id"]: row for row in contacts}
    projection_map = {row["projection_id"]: row for row in projections}
    zero_map = {row["zero_id"]: row for row in zeros}
    bound_map = {row["bound_id"]: row for row in bounds}
    ownership_map = {row["object"]: row for row in ownership}
    decision_map = {row["gate"]: row for row in decisions}

    checkpoint_path = (
        POST
        / "4917-Y5-R2FR-radiative-flow-matter-reentry-coefficients-from-gravity-mediation-or-local-bound-pack.md"
    )
    formal_path = (
        FORMAL
        / "933-PPC4161-gravity-mediated-flow-matter-reentry-and-product-bound.md"
    )
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4917" / "PROVENANCE.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
    provenance = provenance_path.read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(encoding="utf-8")
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8")
    spine = (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-759"
    ]
    variable_rows = [
        row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in VARIABLES
    ]
    variable_sources_exist = all(
        all((ROOT / source).exists() for source in row["source_files"].split(";"))
        for row in variable_rows
    )

    evidence_paths = [OUTPUT / filename for filename in EVIDENCE]
    all_evidence_rows = [row for path in evidence_paths for row in read_csv(path)]
    numeric_cells: list[float] = []
    for row in all_evidence_rows:
        for value in row.values():
            try:
                numeric_cells.append(float(value))
            except (TypeError, ValueError):
                pass
    scripts = [
        SCRIPTS / "Y5_R2FR_4917_radiative_flow_matter_reentry.py",
        SCRIPTS / "Y5_R2FR_4917_radiative_flow_matter_reentry_validation.py",
    ]

    p_bound = bound_map["CONE4917_01_p_mix"]
    product_bound = bound_map["CONE4917_02_aC_enthalpy_product"]
    rows = [
        check(
            "VAL4917_00_prior",
            prior[-1]["check_id"] == "VAL4916_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4916 predecessor validation passes",
        ),
        check(
            "VAL4917_01_channels",
            len(channels) == 4
            and all(bool_cell(row["passed"]) for row in channels),
            "four universal/local channel classifications pass",
        ),
        check(
            "VAL4917_02_massless_nonlocal",
            channel_map["CHAN4917_00_massless_EH_cross"]["momentum_class"]
            == "NONLOCAL_MASSLESS_POLE"
            and not bool_cell(
                channel_map["CHAN4917_00_massless_EH_cross"][
                    "local_flow_coefficient"
                ]
            ),
            "massless Einstein pole is not relabelled as a local flow charge",
        ),
        check(
            "VAL4917_03_contact_basis",
            len(contacts) == 4
            and all(bool_cell(row["passed"]) for row in contacts),
            "total stress square expands to the exact local cross basis",
        ),
        check(
            "VAL4917_04_cross_factors",
            contact_map["CONTACT4917_01_tensor_cross"]["coefficient"]
            == "4 a_C/M_R^4"
            and contact_map["CONTACT4917_02_trace_cross"]["coefficient"]
            == "2(a_R-2a_C/3)/M_R^4",
            "tensor and trace cross factors are fixed without a factor-two loss",
        ),
        check(
            "VAL4917_05_projection",
            len(projections) == 6
            and all(bool_cell(row["passed"]) for row in projections),
            "perfect-fluid and Hilbert metric-shift projections pass",
        ),
        check(
            "VAL4917_06_pmix_factor",
            "-8*a_C" in projection_map["PF4917_00_perfect_fluid"]["p_mix"]
            and "p_X + rho_X"
            in projection_map["PF4917_00_perfect_fluid"]["p_mix"],
            "p_mix carries the derived minus-eight Weyl-enthalpy factor",
        ),
        check(
            "VAL4917_07_vacuum_zero",
            float(projection_map["PF4917_02_vacuum"]["p_mix"]) == 0.0
            and bool_cell(projection_map["PF4917_02_vacuum"]["passed"]),
            "vacuum enthalpy removes the anisotropic flow coefficient",
        ),
        check(
            "VAL4917_08_zero_table",
            len(zeros) == 6 and all(bool_cell(row["passed"]) for row in zeros),
            "coefficient state support and conformal zeros are explicit",
        ),
        check(
            "VAL4917_09_support_zero",
            bool_cell(zero_map["ZERO4917_02_disjoint_support"]["exact_zero"])
            and "entire local" in zero_map["ZERO4917_02_disjoint_support"]["consequence"],
            "positive-gap support theorem remains intact",
        ),
        check(
            "VAL4917_10_bounds",
            len(bounds) == 4 and all(bool_cell(row["passed"]) for row in bounds),
            "cone inversion and product-bound rows pass",
        ),
        check(
            "VAL4917_11_pmix_interval",
            math.isclose(float(p_bound["lower"]), -1.4e-15, rel_tol=1e-12)
            and math.isclose(float(p_bound["upper"]), 6.0e-15, rel_tol=1e-12),
            "exact relative-speed inversion gives the expected signed p_mix interval",
        ),
        check(
            "VAL4917_12_product_interval",
            math.isclose(
                float(product_bound["lower"]), -7.5e-16, rel_tol=1e-12
            )
            and math.isclose(
                float(product_bound["upper"]), 1.75e-16, rel_tol=1e-12
            )
            and math.isclose(
                float(product_bound["absolute_envelope"]),
                7.5e-16,
                rel_tol=1e-12,
            )
            and "delta_c=4" in product_bound["formula"],
            "signed and symmetric no-cancellation product bounds are correct",
        ),
        check(
            "VAL4917_13_bound_scope",
            "no-cancellation" in product_bound["applicability"]
            and "first-order" in product_bound["applicability"],
            "observational map is explicitly conditional rather than a claim",
        ),
        check(
            "VAL4917_14_ownership",
            len(ownership) == 8
            and ownership_map["a_C physical"]["status"] == "OPEN_NUMERIC_TOTAL"
            and ownership_map["anisotropic mixed coefficient"]["status"]
            == "DERIVED_PRODUCT",
            "derived product is separated from the open renormalized coefficient",
        ),
        check(
            "VAL4917_15_scalar_anchor",
            ownership_map["one real scalar a_C loop"]["status"]
            == "DERIVED_COMPONENT_NOT_TOTAL"
            and float(
                ownership_map["one real scalar a_C loop"]["numeric_anchor"]
            )
            > 0,
            "one-real-scalar heat-kernel component is retained only as an anchor",
        ),
        check(
            "VAL4917_16_decisions",
            len(decisions) == 9
            and decision_map["universal_graviton_cross_channel"]["status"]
            == "PASS_NONLOCAL_GR_IDENTIFIED"
            and decision_map["perfect_fluid_flow_projection"]["status"]
            == "PASS_PMIX_MINUS_8_AC_ENTHALPY",
            "channel and projection decisions record the concrete derivation",
        ),
        check(
            "VAL4917_17_open_total",
            decision_map["numeric_coefficient_prediction"]["status"]
            == "OPEN_AC_AR_AND_STATE_PROFILE"
            and decision_map["all_orders_flow_matter_zero"]["status"]
            == "NOT_PROVEN_INDEPENDENT_OPERATORS_REMAIN",
            "unknown parent totals and independent operators are not hidden",
        ),
        check(
            "VAL4917_18_local_GR_scope",
            decision_map["local_GR_status"]["status"]
            == "CONDITIONAL_GR_BRANCH_RETAINED",
            "separated-source local GR is retained without a full all-state claim",
        ),
        check(
            "VAL4917_19_sources",
            len(sources) == 18
            and all(
                bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                and row["sha256"]
                for row in sources
            ),
            "all eighteen local sources markers and hashes resolve",
        ),
        check(
            "VAL4917_20_documents",
            MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_GRAVITY_MEDIATED_REENTRY_PROVENANCE_4917" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4917_21_document_integrity",
            "p_{\\rm mix}=-8a_C(\\rho_X+p_X)/M_R^4" in checkpoint
            and "field basis" in checkpoint
            and "not a second fundamental metric" in checkpoint,
            "checkpoint contains the factor sign and field-redefinition caveat",
        ),
        check(
            "VAL4917_22_claim",
            len(claims) == 1 and claims[0]["status"] == CLAIM_STATUS,
            "L-759 is unique and accurately scoped",
        ),
        check(
            "VAL4917_23_variables",
            len(variable_rows) == len(VARIABLES)
            and {row["symbol"] for row in variable_rows} == set(VARIABLES),
            "ten checkpoint variables are unique",
        ),
        check(
            "VAL4917_24_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4917_25_registers",
            "1.210 Gravity-mediated local stress contact and flow projection"
            in equations
            and "161. A field-redefinition contact is not the massless graviton pole"
            in redteam
            and "PPC4161 checkpoint 4917" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4917_26_resume",
            "4917-Y5-R2FR-radiative-flow-matter-reentry" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume points from the derived product to parent state matching",
        ),
        check(
            "VAL4917_27_csv",
            len(evidence_paths) == 8
            and all(path.exists() and read_csv(path) for path in evidence_paths),
            "eight generated evidence CSVs parse",
        ),
        check(
            "VAL4917_28_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_evidence_rows
                for value in row.values()
            ),
            "generated evidence has no placeholder markers",
        ),
        check(
            "VAL4917_29_finite",
            all(math.isfinite(value) for value in numeric_cells),
            "all parsed numeric evidence cells are finite",
        ),
        check(
            "VAL4917_30_nonclaim",
            all(row.get("valid_for_claim") == "False" for row in all_evidence_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4917_31_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4917_32_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4917_33_next",
            NEXT_TARGET in checkpoint and not (POST / NEXT_TARGET).exists(),
            "4918 parent-state matching target is selected but not pre-created",
        ),
        check(
            "VAL4917_34_no_public_action",
            "No GitHub action or public claim is authorized." in checkpoint,
            "checkpoint remains local and private",
        ),
    ]
    rows.append(
        check(
            "VAL4917_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_GRAVITY_MEDIATED_FLOW_MATTER_REENTRY_4917_VALIDATED",
        )
    )
    return rows


def main() -> int:
    validation = validation_rows()
    write_csv(OUTPUT / "P8_Y5_BRR545_4917_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4917_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4917_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
