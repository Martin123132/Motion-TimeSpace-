from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4885_gamma_memory_uv_operator import NEXT_TARGET, result


CHECKPOINT = "4885"
TIMESTAMP = "2026-07-11T00:06:57+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE_ROOT = POST / "source-intake" / "memory_uv" / "4885"


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
            "SRC4885_00_checkpoint",
            POST
            / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md",
            "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885",
        ),
        (
            "SRC4885_01_research_script",
            POST / "scripts" / "Y5_R2FR_4885_gamma_memory_uv_operator.py",
            "MTS_GAMMA_MEMORY_UV_OPERATOR_4885",
        ),
        (
            "SRC4885_02_gate_script",
            POST
            / "scripts"
            / "Y5_R2FR_4885_gamma_memory_uv_operator_gate.py",
            "P8_Y5_BRR545_4885_VALIDATION_PASS",
        ),
        (
            "SRC4885_03_particle_Gamma",
            ROOT
            / "core-mts-framework"
            / "field-theory"
            / "axio-stable-three-body-bound-states-in-a-dissipative-field-theory.md",
            "dG = saturated_curvature - mu * G",
        ),
        (
            "SRC4885_04_lepton_Gamma",
            ROOT
            / "quantum-particle-field"
            / "leptons-neutrinos"
            / "finite-lepton-families-from-curvature-memory-geometry.md",
            "irreversible",
        ),
        (
            "SRC4885_05_memory_action",
            ROOT
            / "cosmology"
            / "activation-cosmology"
            / "frw-background-and-linear-perturbations-for-the-curvature-memory-field-with-interaction-b-t-m-2.md",
            "+ b T M^2",
        ),
        (
            "SRC4885_06_memory_minimum",
            ROOT
            / "cosmology"
            / "activation-cosmology"
            / "cosmology-branch-of-the-curvature-memory-theory-derived-from-the-action-with-interaction-term-b-t-m-2.md",
            "m_*^2 = 4",
        ),
        (
            "SRC4885_07_open_bath_parent",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "Sigma_R(\\omega)=-i\\gamma\\omega",
        ),
        (
            "SRC4885_08_integrated_metric_parent",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "\\mathcal D\\psi_r",
        ),
        (
            "SRC4885_09_prior_checkpoint",
            POST
            / "4884-Y5-R2FR-strong-matter-contact-coefficient-parent-ownership-or-observational-bound-projection-gate.md",
            "MTS_CONTACT_COEFFICIENT_OWNERSHIP_AND_BOUNDS_4884",
        ),
        (
            "SRC4885_10_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4884_VALIDATION.csv",
            "VAL4884_OVERALL,PASS",
        ),
        (
            "SRC4885_11_formal_note",
            FORMAL
            / "901-PPC4161-Gamma-memory-UV-operator-and-induced-branch-arbitration.md",
            "PPC4161_GAMMA_MEMORY_UV_OPERATOR_4885",
        ),
        (
            "SRC4885_12_claims",
            FORMAL / "02-claims-register.csv",
            "L-727",
        ),
        (
            "SRC4885_13_variables",
            FORMAL / "04-variable-audit.csv",
            "Gamma_M_ownership_4885_MTS",
        ),
        (
            "SRC4885_14_equations",
            FORMAL / "05-equation-register.md",
            "1.178 Canonical memory determinant and overdamped Gamma map",
        ),
        (
            "SRC4885_15_redteam",
            FORMAL / "06-consistency-red-team.md",
            "129. A first-order memory variable is not a second-order UV species",
        ),
        (
            "SRC4885_16_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4885",
        ),
        (
            "SRC4885_17_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_GAMMA_MEMORY_UV_OPERATOR_4885",
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

    pdfs = [
        (
            "SRC4885_18_open_QFT_pdf",
            SOURCE_ROOT / "Crossley_Glorioso_Liu_1511.03646.pdf",
            "C0A23D4C44B72B991843FD52E5FF1F9D747E75906A0E78B50264776D5CAFCC9C",
            "effective field theory of dissipative fluids and closed-time-path constraints",
        ),
        (
            "SRC4885_19_symmetron_pdf",
            SOURCE_ROOT / "Hinterbichler_Khoury_1001.4525.pdf",
            "6141F71035A7474DCCB46DE2D1B87702BF593D920749E06A5A3E9D61D08621A6",
            "density-dependent scalar screening comparison source",
        ),
    ]
    for source_id, path, expected_hash, marker in pdfs:
        exists = path.exists()
        digest = sha256(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_primary_pdf",
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": digest == expected_hash,
                "verification_method": "sha256",
                "sha256": digest,
                "expected_sha256": expected_hash,
            }
        )

    web = [
        (
            "SRC4885_20_open_QFT_web",
            "https://arxiv.org/abs/1511.03646",
            "primary closed-time-path/open-system EFT source",
        ),
        (
            "SRC4885_21_symmetron_web",
            "https://arxiv.org/abs/1001.4525",
            "primary density-dependent scalar screening comparison source",
        ),
        (
            "SRC4885_22_heat_kernel_web",
            "https://arxiv.org/abs/hep-th/0306138",
            "primary heat-kernel review inherited from 4876",
        ),
    ]
    for source_id, url, marker in web:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "web_primary",
                "source_path": url,
                "source_exists": True,
                "marker": marker,
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
        "CORPUS_SIGNATURE": tagged(sections["corpus"]["rows"]),
        "CORPUS_VERDICT": tagged(
            [summary_row(sections["corpus"], {"rows"})]
        ),
        "CANONICAL_HESSIAN": tagged([sections["hessian"]]),
        "OVERDAMPED_MAP": tagged(sections["overdamped"]["rows"]),
        "OVERDAMPED_SUMMARY": tagged(
            [summary_row(sections["overdamped"], {"rows"})]
        ),
        "BATH_XI_NO_GO": tagged(sections["bath_no_go"]["rows"]),
        "BATH_XI_NO_GO_SUMMARY": tagged(
            [summary_row(sections["bath_no_go"], {"rows"})]
        ),
        "TRACE_COUPLING": tagged([sections["trace_coupling"]]),
        "RENORMALIZED_EH_BRANCHES": tagged(sections["fallback"]["rows"]),
        "EH_MATCHING": tagged(sections["fallback"]["matching_rows"]),
        "RENORMALIZED_EH_SUMMARY": tagged(
            [
                summary_row(
                    sections["fallback"], {"rows", "matching_rows"}
                )
            ]
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
    corpus = sections["corpus"]
    hessian = sections["hessian"]
    overdamped = sections["overdamped"]
    bath = sections["bath_no_go"]
    trace = sections["trace_coupling"]
    fallback = sections["fallback"]
    arbitration = sections["arbitration"]
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4884_VALIDATION.csv")

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-727"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    expected_statuses = {
        "M_memory_UV_MTS": (
            "canonical_real_scalar_determinant_candidate_same_parent_join_required"
        ),
        "Gamma_overdamped_MTS": (
            "derived_low_frequency_retarded_readout_of_M"
        ),
        "xi_bath_eff_MTS": (
            "passive_bath_convexity_no_go_negative_xi_not_derived"
        ),
        "bT_to_xi_IR_MTS": (
            "IR_Einstein_trace_correspondence_not_UV_induced_gravity_owner"
        ),
        "mM_scalarization_MTS": (
            "printed_massless_negative_b_branch_local_scalarization_open"
        ),
        "W1_renEH_fallback_MTS": (
            "minimal_three_scalar_U1_W1_negative_renormalized_EH_selected"
        ),
        "Gamma_M_ownership_4885_MTS": (
            "private_partial_UV_determinant_closed_negative_xi_route_demoted"
        ),
    }
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint_path = (
        POST
        / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md"
    )
    formal_path = (
        FORMAL
        / "901-PPC4161-Gamma-memory-UV-operator-and-induced-branch-arbitration.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = formal_path.read_text(encoding="utf-8")
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
        OUTPUT / f"P8_Y5_R2FR_4885_{name}.csv" for name in groups
    ]
    selected = next(
        row
        for row in fallback["rows"]
        if row["branch"] == "complex_psi_plus_M_plus_U1"
    )

    rows = [
        check(
            "VAL4885_00_calculation",
            calculation["all_checks_pass"],
            "all symbolic and numerical sections pass",
        ),
        check(
            "VAL4885_01_sources",
            len(sources) == 23
            and all(row["source_exists"] and row["marker_found"] for row in sources),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4885_02_primary_pdfs",
            all(
                row.get("sha256") == row.get("expected_sha256")
                for row in sources
                if row["source_type"] == "local_primary_pdf"
            ),
            "open-system and screening comparison PDFs hash locked",
        ),
        check(
            "VAL4885_03_prior",
            bool(prior) and all(row["status"] == "PASS" for row in prior),
            "4884 validation remains green",
        ),
        check(
            "VAL4885_04_corpus_signature",
            corpus["passed"]
            and len(corpus["rows"]) == 7
            and corpus["rows"][0]["field_status"]
            == "FIRST_ORDER_RETARDED_MEMORY_VARIABLE"
            and corpus["rows"][2]["field_status"]
            == "COVARIANT_CANONICAL_REAL_SCALAR",
            "Gamma and canonical M are distinguished from source text",
        ),
        check(
            "VAL4885_05_hessian",
            hessian["passed"]
            and hessian["determinant_count"] == 1
            and hessian["kinetic_residue"] == 1.0
            and hessian["minimum_hessian"] == "4*b_abs*rho",
            "one canonical M determinant and density-minimum Hessian",
        ),
        check(
            "VAL4885_06_no_double_count",
            "do not count" in hessian["determinant_rule"]
            and not arbitration["Gamma_first_order_UV_species"],
            "first-order Gamma is not double-counted as a UV scalar",
        ),
        check(
            "VAL4885_07_overdamped_map",
            overdamped["passed"]
            and len(overdamped["rows"]) == 9
            and max(row["relative_response_error"] for row in overdamped["rows"])
            < 1.0e-3,
            "controlled low-frequency Gamma response limit",
        ),
        check(
            "VAL4885_08_gamma_identification",
            "Gamma=g_M*M" in overdamped["Gamma_identification"]
            and "mu=Omega_M^2/gamma_M" in overdamped["Gamma_identification"],
            "Gamma normalization source and decay rate are explicit",
        ),
        check(
            "VAL4885_09_bath_no_go",
            bath["passed"]
            and len(bath["rows"]) == 12
            and all(
                row["nonnegative_inputs_remain_nonnegative"]
                for row in bath["rows"]
            )
            and "cannot generate xi_eff<0" in bath["no_go"],
            "passive nonnegative bath curvature weights obey convexity",
        ),
        check(
            "VAL4885_10_trace_not_UV_xi",
            trace["passed"]
            and not arbitration["bTM2_as_offshell_UV_xi"]
            and "circular" in trace["forbidden_shortcut"],
            "matter trace is not substituted into an induced-G UV operator",
        ),
        check(
            "VAL4885_11_scalarization",
            trace["M_zero_mass_squared_m_minus2"] < 0
            and 30000 < trace["M_zero_tachyon_length_m"] < 30200
            and trace["M_minimum_fluctuation_mass_squared_m_minus2"] > 0,
            "printed anchor moves from unstable zero branch to density-supported branch",
        ),
        check(
            "VAL4885_12_anchor_floor",
            abs(
                trace["M_zero_tachyon_scale_eV"]
                - trace["4884_anchor_stability_floor_eV"]
            )
            < 1.0e-24,
            "trace-coupling and prior curvature-floor calculations agree",
        ),
        check(
            "VAL4885_13_fallback",
            fallback["passed"]
            and selected["W1"] == -1
            and abs(selected["aR_over_aC"] - 1 / 3) < 1.0e-12
            and selected["orders_below_observational_width"] > 70,
            "minimal complex-psi M U1 renormalized-EH fallback",
        ),
        check(
            "VAL4885_14_matching",
            len(fallback["matching_rows"]) == 3
            and all(
                abs(row["MR_squared_over_MbarPl_squared"] - 1) < 1.0e-12
                for row in fallback["matching_rows"]
            )
            and abs(
                fallback["matching_rows"][-1][
                    "M0_squared_over_MbarPl_squared"
                ]
                - 2
            )
            < 1.0e-12,
            "one renormalized Newton calibration closes each sampled cutoff",
        ),
        check(
            "VAL4885_15_arbitration",
            arbitration["passed"]
            and "DEMOTED" in arbitration["three_boson_positive_EH_route"]
            and "RENORMALIZED_EH" in arbitration["selected_local_correspondence_route"]
            and not arbitration["GN_prediction"],
            "pure-induced negative-xi route demoted and honest fallback selected",
        ),
        check(
            "VAL4885_16_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "canonical_M_determinant_and_Gamma_overdamped_map_derived_negative_xi_bath_no_go_three_boson_pure_induced_route_demoted_renormalized_EH_fallback_selected_private_nonclaim",
            "L-727 unique and scope locked",
        ),
        check(
            "VAL4885_17_variables",
            all(
                variable_counts[symbol] == 1
                and variables[symbol]["status"] == status
                for symbol, status in expected_statuses.items()
            ),
            "seven memory-operator variables unique and status locked",
        ),
        check(
            "VAL4885_18_documents",
            "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885"
            in checkpoint
            and "PPC4161_GAMMA_MEMORY_UV_OPERATOR_4885" in formal_note,
            "checkpoint and formal-note markers",
        ),
        check(
            "VAL4885_19_registers",
            "1.178 Canonical memory determinant and overdamped Gamma map"
            in equations
            and "129. A first-order memory variable is not a second-order UV species"
            in redteam
            and "PPC4161 checkpoint 4885" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4885_20_resume",
            "PPC4161_GAMMA_MEMORY_UV_OPERATOR_4885" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4885_21_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4885_22_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence remains private and nonclaim",
        ),
        check(
            "VAL4885_23_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4885_24_scripts",
            compile_source(
                POST / "scripts" / "Y5_R2FR_4885_gamma_memory_uv_operator.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4885_gamma_memory_uv_operator_gate.py"
            ),
            "research and gate scripts compile without bytecode",
        ),
        check(
            "VAL4885_25_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4885_26_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4886 target selected",
        ),
    ]
    rows.append(
        check(
            "VAL4885_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4885_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4885_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4885_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4885_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4885_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
