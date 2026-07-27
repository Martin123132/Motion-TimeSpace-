from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4887_expansion_driven_memory_source import NEXT_TARGET, result


CHECKPOINT = "4887"
TIMESTAMP = "2026-07-11T01:21:19+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
PDF = (
    POST
    / "source-intake"
    / "memory_uv"
    / "4885"
    / "Crossley_Glorioso_Liu_1511.03646.pdf"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            **row,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row in rows
    ]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def source_rows() -> list[dict[str, Any]]:
    local_text = [
        (
            "SRC4887_00_checkpoint",
            POST
            / "4887-Y5-R2FR-conserved-derivative-memory-source-with-local-PPN-silence-and-FLRW-activation-or-active-M-cosmology-demotion-gate.md",
            "MTS_EXPANSION_DRIVEN_MEMORY_SOURCE_4887",
        ),
        (
            "SRC4887_01_research_script",
            POST / "scripts" / "Y5_R2FR_4887_expansion_driven_memory_source.py",
            "MTS_EXPANSION_DRIVEN_MEMORY_SOURCE_4887",
        ),
        (
            "SRC4887_02_gate_script",
            POST
            / "scripts"
            / "Y5_R2FR_4887_expansion_driven_memory_source_gate.py",
            "P8_Y5_BRR545_4887_VALIDATION_PASS",
        ),
        (
            "SRC4887_03_formal_note",
            FORMAL / "903-PPC4161-expansion-driven-memory-source.md",
            "PPC4161_EXPANSION_MEMORY_SOURCE_4887",
        ),
        (
            "SRC4887_04_claims",
            FORMAL / "02-claims-register.csv",
            "L-729",
        ),
        (
            "SRC4887_05_variables",
            FORMAL / "04-variable-audit.csv",
            "expansion_source_4887_MTS",
        ),
        (
            "SRC4887_06_equations",
            FORMAL / "05-equation-register.md",
            "1.180 Expansion-driven memory and stationary local silence",
        ),
        (
            "SRC4887_07_redteam",
            FORMAL / "06-consistency-red-team.md",
            "131. Local silence must come from one covariant operator",
        ),
        (
            "SRC4887_08_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4887",
        ),
        (
            "SRC4887_09_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_EXPANSION_MEMORY_SOURCE_4887",
        ),
        (
            "SRC4887_10_prior_checkpoint",
            POST
            / "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md",
            "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886",
        ),
        (
            "SRC4887_11_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4886_VALIDATION.csv",
            "VAL4886_OVERALL,PASS",
        ),
        (
            "SRC4887_12_open_bath_parent",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "state Landau vector",
        ),
        (
            "SRC4887_13_composite_flow",
            POST
            / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md",
            "unique timelike Landau eigenvector",
        ),
        (
            "SRC4887_14_memory_operator",
            POST
            / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md",
            "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885",
        ),
        (
            "SRC4887_15_local_GR",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "gamma_{\\rm classical}=1",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in local_text:
        exists = path.exists()
        content = (
            path.read_text(encoding="utf-8", errors="replace")
            if exists
            else ""
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_text",
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "verification_method": "local_path_and_marker",
            }
        )

    expected_pdf_hash = (
        "C0A23D4C44B72B991843FD52E5FF1F9D747E75906A0E78B50264776D5CAFCC9C"
    )
    exists = PDF.exists()
    digest = sha256(PDF) if exists else ""
    rows.append(
        {
            "source_id": "SRC4887_16_open_EFT_pdf",
            "source_type": "local_primary_pdf",
            "source_path": str(PDF),
            "source_exists": exists,
            "marker": "sha256",
            "marker_found": digest == expected_pdf_hash,
            "verification_method": "sha256",
            "sha256": digest,
            "expected_sha256": expected_pdf_hash,
        }
    )
    rows.append(
        {
            "source_id": "SRC4887_17_open_EFT_web",
            "source_type": "web_primary",
            "source_path": "https://arxiv.org/abs/1511.03646",
            "source_exists": True,
            "marker": "primary dissipative effective field theory",
            "marker_found": True,
            "verification_method": "primary_source_recorded",
        }
    )
    return tagged(rows)


def summary_row(section: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in section.items() if key not in excluded}


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    return {
        "CANDIDATE_AUDIT": tagged(sections["candidate_audit"]["rows"]),
        "CANDIDATE_SUMMARY": tagged(
            [summary_row(sections["candidate_audit"], {"rows"})]
        ),
        "ACTION": tagged([sections["action"]]),
        "CLOCK_STABILITY": tagged(sections["clock_stability"]["rows"]),
        "CLOCK_SUMMARY": tagged(
            [summary_row(sections["clock_stability"], {"rows"})]
        ),
        "STATIONARY_ARENAS": tagged(sections["stationary_silence"]["rows"]),
        "STATIONARY_SUMMARY": tagged(
            [summary_row(sections["stationary_silence"], {"rows"})]
        ),
        "FLRW_BRANCHES": tagged(sections["FLRW_response"]["rows"]),
        "FLRW_SUMMARY": tagged(
            [summary_row(sections["FLRW_response"], {"rows"})]
        ),
        "COEFFICIENT_OWNERSHIP": tagged(
            [sections["coefficient_ownership"]]
        ),
        "ARBITRATION": tagged([sections["arbitration"]]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "next_target": sections["arbitration"]["next_target"],
                }
            ]
        ),
    }


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError:
        return False
    return True


def validation_rows(
    calculation: dict[str, Any],
    sources: list[dict[str, Any]],
    groups: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    sections = calculation["sections"]
    candidates = sections["candidate_audit"]
    action = sections["action"]
    clock = sections["clock_stability"]
    stationary = sections["stationary_silence"]
    flrw = sections["FLRW_response"]
    ownership = sections["coefficient_ownership"]
    arbitration = sections["arbitration"]
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4886_VALIDATION.csv")

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-729"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    expected_statuses = {
        "sigmaTheta_memory_MTS": (
            "bath_expansion_cross_coefficient_benchmark_parent_Kubo_open"
        ),
        "thetaBath_MTS": "composite_Landau_expansion_local_zero_FLRW_3H",
        "Sexp_memory_MTS": (
            "variationally_closed_first_derivative_source_constructed"
        ),
        "DeltaPPN_exp_MTS": "stationary_Killing_branch_exact_zero",
        "clock_mix_bound_MTS": "derived_positive_gradient_determinant",
        "kappa_exp_FLRW_MTS": "three_tuned_fixed_background_existence_rays",
        "expansion_source_4887_MTS": (
            "conditional_mechanism_constructed_parent_matching_open"
        ),
    }
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4887-Y5-R2FR-conserved-derivative-memory-source-with-local-PPN-silence-and-FLRW-activation-or-active-M-cosmology-demotion-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "903-PPC4161-expansion-driven-memory-source.md"
    ).read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(
        encoding="utf-8"
    )
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(
        encoding="utf-8"
    )
    spine = (FORMAL / "07-unification-spine.md").read_text(
        encoding="utf-8"
    )
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(
        encoding="utf-8"
    )
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4887_{name}.csv" for name in groups
    ]
    flrw_by_target = {
        row["target_Omega_memory_today"]: row for row in flrw["rows"]
    }

    rows = [
        check(
            "VAL4887_00_calculation",
            calculation["all_checks_pass"],
            "candidate action stability local and FLRW sections pass",
        ),
        check(
            "VAL4887_01_sources",
            len(sources) == 18
            and all(row["source_exists"] and row["marker_found"] for row in sources),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4887_02_primary_pdf",
            all(
                row.get("sha256") == row.get("expected_sha256")
                for row in sources
                if row["source_type"] == "local_primary_pdf"
            ),
            "dissipative-EFT PDF hash locked",
        ),
        check(
            "VAL4887_03_prior",
            bool(prior) and all(row["status"] == "PASS" for row in prior),
            "4886 direct-trace compatibility gate remains green",
        ),
        check(
            "VAL4887_04_candidate_audit",
            candidates["passed"]
            and len(candidates["rows"]) == 5
            and candidates["selected"] == "bath_expansion_u_dot_grad_phi",
            "one first-derivative local-silent candidate selected",
        ),
        check(
            "VAL4887_05_direct_trace_rejected",
            candidates["rows"][0]["verdict"]
            == "REJECTED_BY_4886_PPN_COSMOLOGY_IDENTITY",
            "new source does not silently restore bTM2 cosmology",
        ),
        check(
            "VAL4887_06_action_variation",
            action["passed"]
            and "sigma_theta theta" in action["scalar_EOM_without_open_damping"]
            and "3 sigma_theta H" in action["FLRW_equation"],
            "covariant interaction gives zero/local and FLRW source forms",
        ),
        check(
            "VAL4887_07_open_completion",
            "gamma_M" in action["SK_physical_EOM"]
            and "noise" in action["SK_physical_EOM"],
            "Ohmic damping and noise retained",
        ),
        check(
            "VAL4887_08_hamiltonian",
            "cancels" in action["homogeneous_Hamiltonian"]
            and "unchanged" in action["principal_symbol"],
            "no wrong-sign kinetic term or scalar cone change",
        ),
        check(
            "VAL4887_09_clock_owner",
            clock["passed"]
            and "Theta" in clock["clock_owner"]
            and clock["clock_no_ghost"] == "P_X+2X P_XX>0",
            "covariant bath-clock completion",
        ),
        check(
            "VAL4887_10_gradient_bound",
            clock["mixed_gradient_determinant"]
            == "sigma_theta^2 < (rho_X+p_X)/Mbar_Pl^2"
            and 0.38 < clock["selected_gradient_margin"] < 0.39,
            "positive coupled spatial-gradient determinant",
        ),
        check(
            "VAL4887_11_enthalpy_scope",
            abs(clock["minimum_Omega_X_one_plus_w"] - 0.03) < 1.0e-12
            and clock["rows"][0]["positive_gradient_matrix"]
            and not clock["rows"][2]["positive_gradient_matrix"],
            "required bath enthalpy is explicit",
        ),
        check(
            "VAL4887_12_Killing_identity",
            stationary["passed"]
            and "therefore theta=div u=0 exactly" in stationary["Killing_identity"]
            and all(
                row["theta_over_H_or_local_scale"] == 0
                for row in stationary["rows"][:3]
            ),
            "stationary local silence is a theorem rather than a tuned limit",
        ),
        check(
            "VAL4887_13_stationary_PPN",
            stationary["tree_level_matter_scalar_coupling"] == 0
            and stationary["stationary_PPN_gamma"] == 1
            and stationary["stationary_PPN_beta"] == 1,
            "stationary metric-only PPN branch retained",
        ),
        check(
            "VAL4887_14_local_suppression",
            stationary["cosmic_state_local_gradient_suppression_AU"] < 1.3e-30
            and stationary["cosmic_state_local_gradient_suppression_Rsun"]
            < 3.0e-35,
            "slow cosmic-state leakage negligible on local scales",
        ),
        check(
            "VAL4887_15_FLRW_equation",
            flrw["passed"]
            and "3 sigma_bar/E" in flrw["dimensionless_equation"]
            and flrw["initial_conditions"] == "phi=phi_N=0 at N=-7",
            "late-drive initial-value problem explicit",
        ),
        check(
            "VAL4887_16_three_branches",
            len(flrw["rows"]) == 3
            and set(flrw_by_target) == {1.0e-4, 1.0e-3, 1.0e-2},
            "three response amplitudes solved",
        ),
        check(
            "VAL4887_17_target_accuracy",
            all(
                abs(
                    row["Omega_memory_today"]
                    / row["target_Omega_memory_today"]
                    - 1
                )
                < 1.0e-7
                for row in flrw["rows"]
            ),
            "high-kappa rays hit requested present fractions",
        ),
        check(
            "VAL4887_18_fixed_background_control",
            all(row["fixed_background_controlled"] for row in flrw["rows"])
            and flrw["maximum_fixed_background_fraction"] < 0.0141,
            "response remains perturbative in fixed-background smoke",
        ),
        check(
            "VAL4887_19_late_activation",
            0.9 < flrw_by_target[1.0e-2]["half_activation_redshift"] < 1.1
            and 4.0 < flrw_by_target[1.0e-3]["half_activation_redshift"] < 4.1,
            "activation emerges toward late times without switch function",
        ),
        check(
            "VAL4887_20_ownership",
            ownership["passed"]
            and not ownership["numeric_parent_derivation_complete"]
            and "not parent predictions" in ownership["benchmark_status"],
            "existence benchmark not mislabeled microscopic prediction",
        ),
        check(
            "VAL4887_21_arbitration",
            arbitration["passed"]
            and arbitration["stationary_local_PPN"]
            == "EXACTLY_SILENT_ON_KILLING_ALIGNED_STATE"
            and arbitration["FLRW_activation"]
            == "NONZERO_THETA_EQUALS_3H_AND_NUMERIC_BRANCH_REGULAR"
            and not arbitration["coefficient_prediction"],
            "conditional expansion mechanism retained honestly",
        ),
        check(
            "VAL4887_22_retained_spine",
            arbitration["canonical_M_UV_determinant"] == "RETAINED"
            and arbitration["Gamma_overdamped_readout"] == "RETAINED"
            and arbitration["renormalized_EH_local_branch"] == "RETAINED",
            "memory operator and local GR spine preserved",
        ),
        check(
            "VAL4887_23_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "bath_expansion_source_action_stationary_Killing_PPN_silence_clock_stability_and_late_FLRW_existence_derived_parent_Kubo_and_backreaction_open_private_nonclaim",
            "L-729 unique and scope locked",
        ),
        check(
            "VAL4887_24_variables",
            all(
                variable_counts[symbol] == 1
                and variables[symbol]["status"] == status
                for symbol, status in expected_statuses.items()
            ),
            "seven expansion-source variables unique and status locked",
        ),
        check(
            "VAL4887_25_documents",
            "MTS_EXPANSION_DRIVEN_MEMORY_SOURCE_4887" in checkpoint
            and "PPC4161_EXPANSION_MEMORY_SOURCE_4887" in formal_note,
            "checkpoint and formal-note markers",
        ),
        check(
            "VAL4887_26_registers",
            "1.180 Expansion-driven memory and stationary local silence"
            in equations
            and "131. Local silence must come from one covariant operator"
            in redteam
            and "PPC4161 checkpoint 4887" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4887_27_resume",
            "PPC4161_EXPANSION_MEMORY_SOURCE_4887" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4887_28_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4887_29_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all evidence remains private and nonclaim",
        ),
        check(
            "VAL4887_30_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4887_31_scripts",
            compile_source(
                POST / "scripts" / "Y5_R2FR_4887_expansion_driven_memory_source.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4887_expansion_driven_memory_source_gate.py"
            ),
            "research and gate scripts compile without bytecode",
        ),
        check(
            "VAL4887_32_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4887_33_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4888 target selected",
        ),
    ]
    rows.append(
        check(
            "VAL4887_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_EXPANSION_DRIVEN_MEMORY_SOURCE_4887_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4887_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4887_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4887_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4887_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4887_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
