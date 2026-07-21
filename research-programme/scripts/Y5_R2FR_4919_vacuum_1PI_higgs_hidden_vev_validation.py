from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sympy as sp

import Y5_R2FR_4919_vacuum_1PI_higgs_hidden_vev as research


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
    "direct_fixed_metric_hidden_SM_vacuum_portals_zero_curvature_Higgs_"
    "reduced_canonical_alpha_below_one_third_local_range_and_overlap_"
    "contact_bounded_internal_graviton_running_open_private_nonclaim"
)
VARIABLES = (
    "VacuumFactorization4919_MTS",
    "DirectPortalZero4919_MTS",
    "HiddenOddVEV4919_MTS",
    "HiddenEvenCondensate4919_MTS",
    "XiH4919_MTS",
    "HiggsMetricZh4919_MTS",
    "HiggsTraceCoupling4919_MTS",
    "HiggsYukawaStrength4919_MTS",
    "HiggsRange4919_MTS",
    "Vacuum1PIGate4919_MTS",
)
EVIDENCE = (
    "P8_Y5_R2FR_4919_FACTORIZATION.csv",
    "P8_Y5_R2FR_4919_HIDDEN_VACUUM.csv",
    "P8_Y5_R2FR_4919_CURVATURE_HIGGS_BASIS.csv",
    "P8_Y5_R2FR_4919_HIGGS_TRACE_KERNEL.csv",
    "P8_Y5_R2FR_4919_LOCAL_RANGE_PROJECTION.csv",
    "P8_Y5_R2FR_4919_COEFFICIENT_OWNERSHIP.csv",
    "P8_Y5_R2FR_4919_GATE_DECISION.csv",
    "P8_Y5_R2FR_4919_SOURCE_REGISTER.csv",
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

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4918_VALIDATION.csv")
    factors = read_csv(OUTPUT / EVIDENCE[0])
    hidden = read_csv(OUTPUT / EVIDENCE[1])
    basis = read_csv(OUTPUT / EVIDENCE[2])
    kernels = read_csv(OUTPUT / EVIDENCE[3])
    local = read_csv(OUTPUT / EVIDENCE[4])
    ownership = read_csv(OUTPUT / EVIDENCE[5])
    decisions = read_csv(OUTPUT / EVIDENCE[6])
    sources = read_csv(OUTPUT / EVIDENCE[7])

    factor_map = {row["factor_id"]: row for row in factors}
    hidden_map = {row["branch_id"]: row for row in hidden}
    basis_map = {row["basis_id"]: row for row in basis}
    kernel_map = {row["kernel_id"]: row for row in kernels}
    local_map = {row["projection_id"]: row for row in local}
    owner_map = {row["coefficient_id"]: row for row in ownership}
    decision_map = {row["gate"]: row for row in decisions}

    checkpoint_path = (
        POST
        / "4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md"
    )
    formal_path = (
        FORMAL / "935-PPC4161-vacuum-1PI-curvature-Higgs-hidden-vev-gate.md"
    )
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4919" / "PROVENANCE.md"
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
        if row.get("claim_id") == "L-761"
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
        SCRIPTS / "Y5_R2FR_4919_vacuum_1PI_higgs_hidden_vev.py",
        SCRIPTS / "Y5_R2FR_4919_vacuum_1PI_higgs_hidden_vev_validation.py",
    ]
    values = research.calibration()
    symbolic = research.curvature_higgs_symbolics()
    x_symbol = sp.Symbol("x", nonnegative=True)
    local_source_rows = [row for row in sources if bool_cell(row["local_path_required"])]
    external_source_rows = [row for row in sources if not bool_cell(row["local_path_required"])]

    rows = [
        check(
            "VAL4919_00_prior",
            prior[-1]["check_id"] == "VAL4918_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4918 predecessor validation passes",
        ),
        check(
            "VAL4919_01_factor_rows",
            len(factors) == 7 and all(bool_cell(row["passed"]) for row in factors),
            "seven fixed-metric factorization rows pass",
        ),
        check(
            "VAL4919_02_fixed_metric_Hessian",
            factor_map["FACT4919_04_Hessian"]["status"]
            == "EXACT_DIRECT_MIXED_VERTEX_ZERO"
            and float(factor_map["FACT4919_04_Hessian"]["direct_mixed_coefficient"])
            == 0.0,
            "direct fixed-metric mixed Hessian is exactly zero",
        ),
        check(
            "VAL4919_03_vev_factorization",
            factor_map["FACT4919_05_hidden_vev"]["status"]
            == "VEV_CHANGES_PURE_METRIC_MATCHING_NOT_SM_PORTALS",
            "hidden VEV cannot bypass the factorized action",
        ),
        check(
            "VAL4919_04_graviton_boundary",
            factor_map["FACT4919_06_exception"]["status"]
            == "SEPARATE_GRAVITON_MEDIATED_CLASS_OPEN",
            "internal-graviton diagrams are explicitly outside the theorem",
        ),
        check(
            "VAL4919_05_hidden_rows",
            len(hidden) == 6 and all(bool_cell(row["passed"]) for row in hidden),
            "six hidden-vacuum branch rows pass",
        ),
        check(
            "VAL4919_06_motion_zero",
            float(hidden_map["VEV4919_00_motion_scalar"]["odd_vev"]) == 0.0
            and "continuum" in hidden_map["VEV4919_00_motion_scalar"]["caveat"],
            "motion odd VEV zero is branch-scoped with continuum caveat",
        ),
        check(
            "VAL4919_07_memory_branch",
            float(hidden_map["VEV4919_02_memory_scalar"]["odd_vev"]) == 0.0
            and "separate nonzero branch"
            in hidden_map["VEV4919_02_memory_scalar"]["caveat"],
            "memory zero is limited to the selected flat invariant branch",
        ),
        check(
            "VAL4919_08_even_condensate",
            hidden_map["VEV4919_04_even_condensates"]["status"]
            == "PURE_METRIC_MATCHING_ONLY_BY_FACTORIZATION",
            "even condensates need not vanish to close direct portals",
        ),
        check(
            "VAL4919_09_basis_rows",
            len(basis) == 10 and all(bool_cell(row["passed"]) for row in basis),
            "ten curvature-Higgs basis rows pass",
        ),
        check(
            "VAL4919_10_EH_cancellation",
            float(basis_map["BASIS4919_03_EH_cancel"]["symbolic_residual"]) == 0.0
            and symbolic["cancellation"] == 0,
            "metric redefinition cancels the residual curvature monomial",
        ),
        check(
            "VAL4919_11_trace_image",
            basis_map["BASIS4919_04_trace_image"]["status"]
            == "OPERATOR_MOVED_NOT_DELETED"
            and "T_SM" in basis_map["BASIS4919_04_trace_image"]["formula"],
            "correlated Einstein-basis trace operator is retained",
        ),
        check(
            "VAL4919_12_normalization",
            basis_map["BASIS4919_06_normalization"]["status"]
            == "POSITIVE_FOR_REAL_XI_H"
            and symbolic["z_h"] == 1 + 6 * x_symbol,
            "canonical Higgs normalization is positive",
        ),
        check(
            "VAL4919_13_direct_MTS_zero",
            basis_map["BASIS4919_08_direct_MTS"]["status"]
            == "EXACT_DIRECT_MTS_ZERO"
            and float(basis_map["BASIS4919_08_direct_MTS"]["symbolic_residual"])
            == 0.0,
            "direct MTS contribution to xi_H is zero",
        ),
        check(
            "VAL4919_14_total_xi_open",
            basis_map["BASIS4919_09_total_xi"]["status"]
            == "TOTAL_COEFFICIENT_OPEN_NOT_SET_TO_ZERO",
            "total renormalized xi_H is not falsely set to zero",
        ),
        check(
            "VAL4919_15_kernel_rows",
            len(kernels) == 8 and all(bool_cell(row["passed"]) for row in kernels),
            "eight physical Higgs-kernel rows pass",
        ),
        check(
            "VAL4919_16_alpha_identity",
            sp.simplify(symbolic["alpha"] - 2 * x_symbol / (1 + 6 * x_symbol))
            == 0
            and sp.simplify(
                symbolic["alpha_margin"] - 1 / (3 * (1 + 6 * x_symbol))
            )
            == 0,
            "alpha_xi is bounded below one third for nonnegative x",
        ),
        check(
            "VAL4919_17_alpha_envelope",
            math.isclose(
                float(kernel_map["KERNEL4919_02_alpha"]["numeric_value"]),
                1.0 / 3.0,
                rel_tol=1e-15,
            ),
            "numeric alpha envelope is one third",
        ),
        check(
            "VAL4919_18_gxi_envelope",
            math.isclose(
                float(kernel_map["KERNEL4919_01_gxi"]["numeric_value"]),
                2.81018845153841e-38,
                rel_tol=1e-13,
            ),
            "canonical trace coupling-square envelope is calibrated",
        ),
        check(
            "VAL4919_19_Higgs_range",
            math.isclose(values["lambda_h_m"], 1.5769757888540122e-18, rel_tol=1e-13)
            and math.isclose(
                float(kernel_map["KERNEL4919_03_pole"]["numeric_value"]),
                values["lambda_h_m"],
                rel_tol=1e-15,
            ),
            "125.13 GeV Higgs range is correctly converted",
        ),
        check(
            "VAL4919_20_lowq_contact",
            math.isclose(
                float(kernel_map["KERNEL4919_04_low_q"]["numeric_value"]),
                8.973927569378546e-43,
                rel_tol=1e-13,
            ),
            "coefficient-independent low-q contact envelope is correct",
        ),
        check(
            "VAL4919_21_historical_quarantine",
            kernel_map["KERNEL4919_06_historical"]["status"]
            == "SOURCE_BACKED_CROSSCHECK_NOT_CURRENT_GATE",
            "2012 collider result is quarantined as a historical comparator",
        ),
        check(
            "VAL4919_22_local_rows",
            len(local) == 9 and all(bool_cell(row["passed"]) for row in local),
            "nine exterior contact clock WEP and Maxwell projections pass",
        ),
        check(
            "VAL4919_23_femtometre",
            math.isclose(
                float(local_map["LOCAL4919_01_femtometre"]["log10_point_force_ratio_upper"]),
                -273.0713130459303,
                rel_tol=1e-13,
            ),
            "one-femtometre full-pole force bound is underflow-safe",
        ),
        check(
            "VAL4919_24_R10",
            math.isclose(
                float(local_map["LOCAL4919_03_R10"]["log10_point_force_ratio_upper"]),
                -14320646657080.139,
                rel_tol=1e-13,
            ),
            "R10 full-pole force bound is derived in logarithms",
        ),
        check(
            "VAL4919_25_contact_support",
            local_map["LOCAL4919_03_R10"]["contact_cross_support"]
            == "exact_zero_in_low_q_contact_expansion",
            "low-q contact has zero cross support across a positive gap",
        ),
        check(
            "VAL4919_26_lab_clock",
            math.isclose(
                float(local_map["LOCAL4919_06_lab_clock_contact"]["contact_cross_support"]),
                2.3207279524452717e-58,
                rel_tol=1e-13,
            ),
            "overlapping laboratory clock/mass shift is bounded",
        ),
        check(
            "VAL4919_27_lab_self",
            math.isclose(
                float(local_map["LOCAL4919_07_lab_WEP_self"]["contact_cross_support"]),
                1.1603639762226358e-58,
                rel_tol=1e-13,
            ),
            "overlapping contact self-energy is bounded rather than erased",
        ),
        check(
            "VAL4919_28_Maxwell",
            local_map["LOCAL4919_08_Maxwell"]["contact_cross_support"]
            == "T_Maxwell=0 in four classical dimensions",
            "classical Maxwell trace projection is zero",
        ),
        check(
            "VAL4919_29_ownership_rows",
            len(ownership) == 7 and all(bool_cell(row["passed"]) for row in ownership),
            "seven coefficient-ownership rows pass",
        ),
        check(
            "VAL4919_30_owner_direct",
            owner_map["OWN4919_00_xi_direct_MTS"]["promotion"]
            == "EXACT_ZERO_ON_ACTIVE_PARENT"
            and float(owner_map["OWN4919_00_xi_direct_MTS"]["value_or_status"])
            == 0.0,
            "direct and total xi_H ownership are separated",
        ),
        check(
            "VAL4919_31_owner_graviton",
            owner_map["OWN4919_02_xi_gravity"]["promotion"] == "NEXT_CHECKPOINT",
            "graviton-mediated coefficient is explicitly open",
        ),
        check(
            "VAL4919_32_decisions",
            len(decisions) == 9
            and decision_map["direct_fixed_metric_vacuum_portal"]["status"]
            == "CLOSED_EXACTLY_BY_FACTORIZATION"
            and decision_map["curvature_Higgs_basis"]["status"]
            == "REDUCED_TO_CANONICAL_HIGGS_TRACE_KERNEL",
            "direct portal and curvature-Higgs decisions are explicit",
        ),
        check(
            "VAL4919_33_local_decision",
            decision_map["R10_PPN_clock_orbit"]["status"]
            == "PASS_FOR_CURVATURE_HIGGS_CHANNEL",
            "local pass is limited to the curvature-Higgs channel",
        ),
        check(
            "VAL4919_34_next_decision",
            decision_map["full_vacuum_1PI"]["status"]
            == "DIRECT_PORTALS_CLOSED_GRAVITON_MEDIATED_RUNNING_OPEN"
            and decision_map["full_vacuum_1PI"]["decision"] == NEXT_TARGET,
            "next target advances to internal-graviton running",
        ),
        check(
            "VAL4919_35_sources",
            len(sources) == 32
            and len(local_source_rows) == 28
            and len(external_source_rows) == 4
            and all(
                bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                and row["sha256"]
                for row in sources
            ),
            "all thirty-two local and external provenance rows resolve",
        ),
        check(
            "VAL4919_36_local_hashes",
            all(
                row["sha256"] != "external_source_not_hashed"
                for row in local_source_rows
            )
            and all(
                row["sha256"] == "external_source_not_hashed"
                for row in external_source_rows
            ),
            "local sources are hashed and external sources are labelled",
        ),
        check(
            "VAL4919_37_external_urls",
            {row["source_path_or_url"] for row in external_source_rows}
            == {
                research.PDG_HIGGS_URL,
                research.NIST_FERMI_URL,
                research.ATKINS_CALMET_URL,
                research.EOTWASH_URL,
            },
            "official and primary external URLs are locked",
        ),
        check(
            "VAL4919_38_documents",
            MARKER in checkpoint
            and research.FORMAL_MARKER in formal_note
            and "MTS_VACUUM_1PI_HIGGS_PROVENANCE_4919" in provenance,
            "checkpoint formal note and provenance markers exist",
        ),
        check(
            "VAL4919_39_document_integrity",
            "operator has moved basis; it has not disappeared" in checkpoint
            and "alpha_\\xi" in checkpoint
            and "internal-graviton" in checkpoint
            and "1.16036e-58" in checkpoint,
            "document preserves basis range overlap and graviton caveats",
        ),
        check(
            "VAL4919_40_claim",
            len(claims) == 1 and claims[0]["status"] == CLAIM_STATUS,
            "L-761 is unique and accurately scoped",
        ),
        check(
            "VAL4919_41_variables",
            len(variable_rows) == len(VARIABLES)
            and {row["symbol"] for row in variable_rows} == set(VARIABLES),
            "ten checkpoint variables are unique",
        ),
        check(
            "VAL4919_42_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4919_43_registers",
            "1.212 Vacuum 1PI factorization and curvature-Higgs reduction" in equations
            and "163. A removable curvature-Higgs monomial is not a vanishing physical channel"
            in redteam
            and "PPC4161 checkpoint 4919" in spine,
            "equation red-team and spine registers are updated",
        ),
        check(
            "VAL4919_44_resume",
            "4919-Y5-R2FR-vacuum-1PI" in resume
            and research.FORMAL_MARKER in resume
            and NEXT_TARGET in resume,
            "resume points from direct-portal closure to graviton running",
        ),
        check(
            "VAL4919_45_csv",
            len(evidence_paths) == 8
            and all(path.exists() and read_csv(path) for path in evidence_paths),
            "eight generated evidence CSVs parse",
        ),
        check(
            "VAL4919_46_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_evidence_rows
                for value in row.values()
            ),
            "generated evidence has no placeholder markers",
        ),
        check(
            "VAL4919_47_finite",
            all(math.isfinite(value) for value in numeric_cells),
            "all parsed numeric evidence cells are finite",
        ),
        check(
            "VAL4919_48_nonclaim",
            all(row.get("valid_for_claim") == "False" for row in all_evidence_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4919_49_scripts",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile",
        ),
        check(
            "VAL4919_50_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no scripts pycache exists",
        ),
        check(
            "VAL4919_51_next",
            NEXT_TARGET in checkpoint and not (POST / NEXT_TARGET).exists(),
            "4920 graviton-running target is selected but not pre-created",
        ),
        check(
            "VAL4919_52_no_public_action",
            "No GitHub action or public claim is authorized." in checkpoint,
            "checkpoint remains local and private",
        ),
    ]
    rows.append(
        check(
            "VAL4919_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_VACUUM_1PI_HIGGS_HIDDEN_VEV_GATE_4919_VALIDATED",
        )
    )
    return rows


def main() -> int:
    validation = validation_rows()
    write_csv(OUTPUT / "P8_Y5_BRR545_4919_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4919_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4919_VALIDATION_FAIL"
    )
    if not passed:
        for row in validation:
            if row["status"] != "PASS":
                print(row["check_id"], row["detail"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
