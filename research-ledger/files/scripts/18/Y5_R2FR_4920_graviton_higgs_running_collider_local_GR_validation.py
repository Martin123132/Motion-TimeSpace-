from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Y5_R2FR_4920_graviton_higgs_running_collider_local_GR as research


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUTPUT = POST / "source-intake" / "mts_residuals"
TIMESTAMP = datetime.now(timezone.utc).isoformat()
MARKER = research.MARKER
FORMAL_MARKER = research.FORMAL_MARKER
NEXT_TARGET = research.NEXT_TARGET
VARIABLES = (
    "GravXiPacket4920_MTS",
    "XiTotal4920_MTS",
    "HiggsBeta4920_MTS",
    "HiggsKappa4920_MTS",
    "HiggsMu4920_MTS",
    "XiProfileLimit4920_MTS",
    "LambdaXi4920_MTS",
    "EpsilonXi4920_MTS",
    "VacuumLocalGRCertificate4920_MTS",
    "PureMetricResidualGate4920_MTS",
)
EVIDENCE = (
    "P8_Y5_R2FR_4920_RUNNING_BASIS.csv",
    "P8_Y5_R2FR_4920_HIGGS_INPUTS.csv",
    "P8_Y5_R2FR_4920_COLLIDER_RECAST.csv",
    "P8_Y5_R2FR_4920_EFT_CUTOFF.csv",
    "P8_Y5_R2FR_4920_LOCAL_LOOP_PROJECTION.csv",
    "P8_Y5_R2FR_4920_PROMOTION_DOMAIN.csv",
    "P8_Y5_R2FR_4920_GATE_DECISION.csv",
    "P8_Y5_R2FR_4920_SOURCE_REGISTER.csv",
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


def close(left: float, right: float, rel: float = 1.0e-12) -> bool:
    return math.isclose(left, right, rel_tol=rel, abs_tol=0.0)


def validation_rows() -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4919_VALIDATION.csv")
    running = read_csv(OUTPUT / EVIDENCE[0])
    inputs = read_csv(OUTPUT / EVIDENCE[1])
    recasts = read_csv(OUTPUT / EVIDENCE[2])
    cutoffs = read_csv(OUTPUT / EVIDENCE[3])
    loops = read_csv(OUTPUT / EVIDENCE[4])
    domains = read_csv(OUTPUT / EVIDENCE[5])
    decisions = read_csv(OUTPUT / EVIDENCE[6])
    sources = read_csv(OUTPUT / EVIDENCE[7])

    running_map = {row["basis_id"]: row for row in running}
    input_map = {row["input_id"]: row for row in inputs}
    recast_map = {row["recast_id"]: row for row in recasts}
    cutoff_map = {row["cutoff_id"]: row for row in cutoffs}
    loop_map = {row["projection_id"]: row for row in loops}
    domain_map = {row["domain_id"]: row for row in domains}
    decision_map = {row["gate"]: row for row in decisions}

    checkpoint_path = POST / (
        "4920-Y5-R2FR-graviton-mediated-curvature-Higgs-running-and-current-"
        "Higgs-coupling-bound-or-vacuum-local-GR-promotion-gate.md"
    )
    formal_path = FORMAL / (
        "936-PPC4161-graviton-Higgs-observable-bound-vacuum-local-GR-"
        "promotion.md"
    )
    provenance_path = (
        POST / "source-intake" / "parent_coupling" / "4920" / "PROVENANCE.md"
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
        if row.get("claim_id") == "L-762"
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

    atlas_expected = research.profile_limit(
        research.ATLAS_MU,
        research.ATLAS_SIGMA_MINUS,
        research.ONE_SIDED_95_DELTA_CHI2,
    )
    cms_expected = research.profile_limit(
        research.CMS_MU,
        research.CMS_SIGMA_MINUS,
        research.ONE_SIDED_95_DELTA_CHI2,
    )
    atlas_two_expected = research.profile_limit(
        research.ATLAS_MU,
        research.ATLAS_SIGMA_MINUS,
        research.TWO_SIDED_95_DELTA_CHI2,
    )
    atlas_row = recast_map["RECAST4920_ATLAS_one_sided_95"]
    cms_row = recast_map["RECAST4920_CMS_one_sided_95"]
    atlas_two_row = recast_map["RECAST4920_ATLAS_two_sided_95_envelope"]
    local_source_rows = [row for row in sources if bool_cell(row["local_path_required"])]
    external_source_rows = [
        row for row in sources if not bool_cell(row["local_path_required"])
    ]
    scripts = [
        SCRIPTS / "Y5_R2FR_4920_graviton_higgs_running_collider_local_GR.py",
        SCRIPTS
        / "Y5_R2FR_4920_graviton_higgs_running_collider_local_GR_validation.py",
    ]

    rows = [
        check(
            "VAL4920_00_prior",
            prior[-1]["check_id"] == "VAL4919_OVERALL"
            and prior[-1]["status"] == "PASS",
            "4919 predecessor validation passes",
        ),
        check(
            "VAL4920_01_running_rows",
            len(running) == 10 and all(bool_cell(row["passed"]) for row in running),
            "ten running and field-basis rows pass",
        ),
        check(
            "VAL4920_02_internal_graviton_boundary",
            running_map["RUN4920_00_boundary"]["invariant_status"]
            == "EXPLICIT_EXCEPTION_INHERITED_FROM_4919",
            "internal graviton diagrams are retained",
        ),
        check(
            "VAL4920_03_analytic_nonanalytic_split",
            "Gamma_grav=Gamma_local_analytic+Gamma_nonanalytic"
            in running_map["RUN4920_01_split"]["statement"],
            "analytic and nonanalytic classes are explicitly split",
        ),
        check(
            "VAL4920_04_beta_not_observable",
            running_map["RUN4920_02_xi_beta"]["invariant_status"]
            == "NOT_A_STANDALONE_OBSERVABLE",
            "naked beta_xi is not used as an invariant gate",
        ),
        check(
            "VAL4920_05_packet_not_deleted",
            running_map["RUN4920_03_redefinition"]["invariant_status"]
            == "OPERATOR_MOVED_NOT_ERASED",
            "field redefinition preserves the correlated packet",
        ),
        check(
            "VAL4920_06_nonanalytic_retained",
            running_map["RUN4920_07_nonanalytic"]["invariant_status"]
            == "PHYSICAL_LONG_RANGE_CLASS",
            "nonanalytic amplitude is retained as physical",
        ),
        check(
            "VAL4920_07_input_rows",
            len(inputs) == 4 and all(bool_cell(row["passed"]) for row in inputs),
            "four current-data and model-contract rows pass",
        ),
        check(
            "VAL4920_08_ATLAS_input",
            float(input_map["HIGGS4920_00_ATLAS"]["mu_observed"])
            == research.ATLAS_MU
            and float(input_map["HIGGS4920_00_ATLAS"]["sigma_minus"])
            == research.ATLAS_SIGMA_MINUS,
            "ATLAS current global signal strength is exact",
        ),
        check(
            "VAL4920_09_CMS_input",
            float(input_map["HIGGS4920_01_CMS"]["mu_observed"])
            == research.CMS_MU
            and "2026" in input_map["HIGGS4920_01_CMS"]["analysis"],
            "CMS 2026 current comprehensive combination is used",
        ),
        check(
            "VAL4920_10_no_fake_combination",
            input_map["HIGGS4920_03_no_combine"]["status"]
            == "NO_UNPUBLISHED_COVARIANCE_OR_LIKELIHOOD_COMBINATION",
            "ATLAS and CMS are not combined",
        ),
        check(
            "VAL4920_11_recast_rows",
            len(recasts) == 4 and all(bool_cell(row["passed"]) for row in recasts),
            "four individual recast rows pass",
        ),
        check(
            "VAL4920_12_physical_boundary",
            all(float(row["physical_best_mu"]) == 1.0 for row in recasts),
            "all physical best fits are at mu=1",
        ),
        check(
            "VAL4920_13_ATLAS_mu_limit",
            close(float(atlas_row["mu_lower"]), atlas_expected["mu_lower"]),
            "ATLAS lower signal-strength limit reproduces the profile formula",
        ),
        check(
            "VAL4920_14_ATLAS_xi_limit",
            close(float(atlas_row["abs_xi_upper"]), atlas_expected["xi_upper"]),
            "ATLAS xi limit reproduces the profile formula",
        ),
        check(
            "VAL4920_15_CMS_xi_limit",
            close(float(cms_row["abs_xi_upper"]), cms_expected["xi_upper"]),
            "CMS xi limit reproduces the profile formula",
        ),
        check(
            "VAL4920_16_ATLAS_stronger",
            float(atlas_row["abs_xi_upper"]) < float(cms_row["abs_xi_upper"]),
            "ATLAS is the stronger individual one-sided input",
        ),
        check(
            "VAL4920_17_recast_nonofficial",
            all("NOT_OFFICIAL" in row["likelihood_status"] for row in recasts),
            "every recast row is labelled nonofficial",
        ),
        check(
            "VAL4920_18_two_sided_envelope",
            close(
                float(atlas_two_row["abs_xi_upper"]),
                atlas_two_expected["xi_upper"],
            )
            and float(atlas_two_row["abs_xi_upper"])
            > float(atlas_row["abs_xi_upper"]),
            "two-sided comparator is the looser envelope",
        ),
        check(
            "VAL4920_19_cutoff_rows",
            len(cutoffs) == 4 and all(bool_cell(row["passed"]) for row in cutoffs),
            "four cutoff rows pass",
        ),
        check(
            "VAL4920_20_cutoff_recomputed",
            close(
                float(
                    cutoff_map["CUTOFF4920_ATLAS_two_sided"][
                        "Lambda_vacuum_M_over_xi_GeV"
                    ]
                ),
                atlas_two_expected["cutoff_M_over_xi_GeV"],
            ),
            "conservative ATLAS vacuum cutoff is recomputed",
        ),
        check(
            "VAL4920_21_Higgs_below_cutoff",
            research.HIGGS_MASS_GEV
            < float(
                cutoff_map["CUTOFF4920_ATLAS_two_sided"][
                    "Lambda_vacuum_M_over_xi_GeV"
                ]
            ),
            "on-shell Higgs scale lies below the conservative cutoff",
        ),
        check(
            "VAL4920_22_loop_rows",
            len(loops) == 9 and all(bool_cell(row["passed"]) for row in loops),
            "nine local loop projections pass",
        ),
        check(
            "VAL4920_23_Higgs_loop_control",
            float(loop_map["LOOP4920_Higgs_pole"]["epsilon_xi_NDA"]) < 1.0e-4,
            "Higgs-pole loop expansion is perturbative",
        ),
        check(
            "VAL4920_24_R10_loop_bound",
            float(loop_map["LOOP4920_R10_52um"]["epsilon_xi_NDA"])
            < 1.0e-30,
            "R10 xi-enhanced loop envelope is negligible",
        ),
        check(
            "VAL4920_25_optical_loop_bound",
            float(loop_map["LOOP4920_optical_EM_1eV"]["epsilon_xi_NDA"])
            < 1.0e-20,
            "optical Maxwell loop envelope is negligible",
        ),
        check(
            "VAL4920_26_atomic_loop_bound",
            float(loop_map["LOOP4920_atomic_1A"]["epsilon_xi_NDA"])
            < 1.0e-18,
            "atomic loop envelope is negligible",
        ),
        check(
            "VAL4920_27_solar_loop_bound",
            float(loop_map["LOOP4920_solar_radius"]["epsilon_xi_NDA"])
            < 1.0e-55,
            "solar PPN loop envelope is negligible",
        ),
        check(
            "VAL4920_28_orbit_loop_bound",
            float(loop_map["LOOP4920_one_AU"]["epsilon_xi_NDA"])
            < 1.0e-60,
            "orbital loop envelope is negligible",
        ),
        check(
            "VAL4920_29_loop_is_NDA",
            all("NDA_ENVELOPE" in row["status"] for row in loops),
            "loop values are never labelled exact coefficients",
        ),
        check(
            "VAL4920_30_analytic_support",
            all(row["analytic_support"] == "renormalized_local_or_contact" for row in loops),
            "analytic class remains local or contact supported",
        ),
        check(
            "VAL4920_31_domain_rows",
            len(domains) == 9 and all(bool_cell(row["passed"]) for row in domains),
            "nine promotion-domain clauses pass",
        ),
        check(
            "VAL4920_32_state_scope",
            "invariant vacuum only" in domain_map["DOMAIN4920_01_state"]["scope"],
            "promotion is state scoped",
        ),
        check(
            "VAL4920_33_weak_scope",
            domain_map["DOMAIN4920_05_weak_GR"]["status"]
            == "PRIVATE_1PN_CERTIFICATE_4879_RETAINED",
            "weak 1PN certificate is inherited explicitly",
        ),
        check(
            "VAL4920_34_pure_metric_separate",
            domain_map["DOMAIN4920_07_pure_metric"]["status"]
            == "SEPARATE_ACTIVE_LEDGER_NOT_ERASED",
            "pure-metric residuals remain separate",
        ),
        check(
            "VAL4920_35_decision_rows",
            len(decisions) == 8,
            "eight gate decisions are recorded",
        ),
        check(
            "VAL4920_36_private_promotion",
            decision_map["invariant_vacuum_weak_field_local_GR"]["status"]
            == "PROMOTED_PRIVATE_CONDITIONAL_CERTIFICATE",
            "selected vacuum weak branch is promoted privately and conditionally",
        ),
        check(
            "VAL4920_37_full_theory_not_promoted",
            decision_map["full_MTS_to_GR"]["status"] == "NOT_PROMOTED",
            "full MTS-to-GR claim remains false",
        ),
        check(
            "VAL4920_38_next_target",
            decision_map["next_target"]["decision"] == NEXT_TARGET,
            "pure-metric residual gate is the direct next target",
        ),
        check(
            "VAL4920_39_checkpoint_marker",
            MARKER in checkpoint and "abs(xi_total) < 1.0841e15" in checkpoint,
            "checkpoint contains marker and primary result",
        ),
        check(
            "VAL4920_40_formal_marker",
            FORMAL_MARKER in formal_note and "1.99976 TeV" in formal_note,
            "formal note contains marker and cutoff",
        ),
        check(
            "VAL4920_41_provenance",
            "MTS_GRAVITON_HIGGS_PROVENANCE_4920" in provenance
            and research.ATLAS_URL in provenance
            and research.CMS_URL in provenance,
            "provenance records both current experimental sources",
        ),
        check(
            "VAL4920_42_claim",
            len(claims) == 1 and "private_conditional" in claims[0]["status"],
            "claim L-762 is unique and nonpublic",
        ),
        check(
            "VAL4920_43_variables",
            len(variable_rows) == len(VARIABLES)
            and len({row["symbol"] for row in variable_rows}) == len(VARIABLES),
            "ten checkpoint variables are unique",
        ),
        check(
            "VAL4920_44_variable_sources",
            variable_sources_exist,
            "all variable source paths exist",
        ),
        check(
            "VAL4920_45_equation",
            "1.213 Graviton-Higgs observable packet and local loop bound" in equations,
            "equation-register section 1.213 exists",
        ),
        check(
            "VAL4920_46_redteam",
            "164. A running Jordan-basis coefficient is not an on-shell local-gravity observable"
            in redteam,
            "red-team section 164 exists",
        ),
        check(
            "VAL4920_47_spine",
            "PPC4161 checkpoint 4920" in spine and FORMAL_MARKER in spine,
            "unification spine contains checkpoint 4920",
        ),
        check(
            "VAL4920_48_resume",
            FORMAL_MARKER in resume and NEXT_TARGET in resume,
            "current resume advances to checkpoint 4921",
        ),
        check(
            "VAL4920_49_local_sources",
            len(local_source_rows) == 18
            and all(
                bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                and Path(row["source_path_or_url"]).exists()
                for row in local_source_rows
            ),
            "all 18 local source paths and markers validate",
        ),
        check(
            "VAL4920_50_external_sources",
            len(external_source_rows) == 5
            and all(
                row["source_path_or_url"].startswith("https://")
                and bool_cell(row["source_exists"])
                and bool_cell(row["marker_found"])
                for row in external_source_rows
            ),
            "five external primary source rows are complete",
        ),
        check(
            "VAL4920_51_evidence_files",
            all(path.exists() and path.stat().st_size > 0 for path in evidence_paths),
            "all eight evidence tables exist and are nonempty",
        ),
        check(
            "VAL4920_52_nonclaim",
            all(not bool_cell(row["valid_for_claim"]) for row in all_evidence_rows),
            "every evidence row remains nonclaim",
        ),
        check(
            "VAL4920_53_no_missing_markers",
            all(
                "MISSING_" not in str(value)
                for row in all_evidence_rows
                for value in row.values()
            ),
            "no placeholder marker appears in evidence",
        ),
        check(
            "VAL4920_54_numeric_finite",
            bool(numeric_cells) and all(math.isfinite(value) for value in numeric_cells),
            "all parseable numeric evidence cells are finite",
        ),
        check(
            "VAL4920_55_scripts_compile",
            all(compile_source(path) for path in scripts),
            "research and validation scripts compile without py_compile",
        ),
        check(
            "VAL4920_56_no_pycache",
            not any(path.name == "__pycache__" for path in SCRIPTS.iterdir()),
            "scripts directory contains no __pycache__",
        ),
        check(
            "VAL4920_57_no_control_CR",
            all("\r" not in text for text in (checkpoint, formal_note, provenance)),
            "new Markdown sources contain no embedded carriage-return control characters",
        ),
    ]
    rows.append(
        check(
            "VAL4920_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "all checkpoint-4920 validation gates pass",
        )
    )
    return rows


def main() -> int:
    rows = validation_rows()
    output_path = OUTPUT / "P8_Y5_BRR545_4920_VALIDATION.csv"
    write_csv(output_path, rows)
    failures = [row for row in rows if row["status"] != "PASS"]
    print(f"P8_Y5_BRR545_4920_VALIDATION rows={len(rows)} failures={len(failures)}")
    for failure in failures:
        print(f"{failure['check_id']}: {failure['detail']}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
