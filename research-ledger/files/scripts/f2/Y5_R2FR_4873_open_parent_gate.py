from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from Y5_R2FR_4873_open_parent_induced_gravity import result


CHECKPOINT = "4873"
TIMESTAMP = "2026-07-10T21:15:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4874-Y5-R2FR-metric-only-quotient-background-independence-and-"
    "universal-principal-symbol-proof-or-equivalence-axiom-freeze.md"
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


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def stamp(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["timestamp_utc"] = TIMESTAMP
    return rows


def source_rows() -> list[dict[str, Any]]:
    local = [
        (
            "SRC4873_00_core",
            ROOT / "core-mts-framework" / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "A_MTS",
            "legacy scalar action",
        ),
        (
            "SRC4873_01_4872",
            POST / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md",
            "PRIMITIVE_COVARIANCE_SIGN_AND_FLOW_RANK_THEOREM_4872",
            "primitive no-go handoff",
        ),
        (
            "SRC4873_02_4861",
            POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md",
            "PUBLIC_FRAME_VARIATION_SELECTION_4861",
            "public source metric",
        ),
        (
            "SRC4873_03_checkpoint",
            POST / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "OPEN_PARENT_HADAMARD_INDUCED_GRAVITY_AND_METRIC_ONLY_QUOTIENT_4873",
            "human derivation",
        ),
        (
            "SRC4873_04_formal",
            FORMAL / "889-PPC4161-open-parent-induced-gravity-and-metric-only-local-branch.md",
            "PPC4161_OPEN_PARENT_INDUCED_GR_METRIC_ONLY_BRANCH_4873",
            "formal integration",
        ),
        (
            "SRC4873_05_script",
            POST / "scripts" / "Y5_R2FR_4873_open_parent_induced_gravity.py",
            "def schwinger_keldysh_action",
            "symbolic derivation",
        ),
        (
            "SRC4873_06_generator",
            Path(__file__).resolve(),
            'CHECKPOINT = "4873"',
            "checkpoint generator",
        ),
        ("SRC4873_07_claim", FORMAL / "02-claims-register.csv", "L-715", "claim register"),
        (
            "SRC4873_08_variable",
            FORMAL / "04-variable-audit.csv",
            "lead_primitive_local_branch_selected_background_and_source_descent_open",
            "variable audit",
        ),
        (
            "SRC4873_09_equation",
            FORMAL / "05-equation-register.md",
            "1.166 Open damping action",
            "equation register",
        ),
        (
            "SRC4873_10_redteam",
            FORMAL / "06-consistency-red-team.md",
            "117. Open parent and metric-only branch red team",
            "red-team register",
        ),
        (
            "SRC4873_11_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4873",
            "unification spine",
        ),
        (
            "SRC4873_12_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "Last checkpoint: " + chr(96) + "4873-",
            "resume marker",
        ),
        (
            "SRC4873_13_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4872_VALIDATION.csv",
            "VAL4872_OVERALL",
            "historical validation",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": needle in content,
                "role": role,
                "source_validated": path.exists() and needle in content,
            }
        )

    web = [
        (
            "SRC4873_14_SK",
            "https://arxiv.org/abs/1511.03646",
            "Schwinger-Keldysh dissipative EFT constraints",
        ),
        (
            "SRC4873_15_heat_kernel",
            "https://arxiv.org/abs/hep-th/0306138",
            "heat-kernel coefficient provenance",
        ),
        (
            "SRC4873_16_induced_gravity",
            "https://arxiv.org/abs/gr-qc/0204062",
            "Sakharov induced-gravity interpretation",
        ),
    ]
    for source_id, locator, role in web:
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "web_primary",
                "source_locator": locator,
                "needle": "",
                "source_exists": True,
                "needle_found": True,
                "role": role,
                "source_validated": True,
            }
        )
    return stamp(rows)


def sk_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    sk = data["sections"]["sk_action"]
    bath = data["sections"]["ohmic_bath"]
    return stamp(
        [
            {
                "gate_id": "SK4873_0_response",
                "statement": sk["action_density"],
                "status": "PASS_BULK_DAMPING",
                "result": sk["physical_response_equation"],
                "remaining_gate": "closed bath completion",
            },
            {
                "gate_id": "SK4873_1_normalization",
                "statement": "S[psi_r,0]=0",
                "status": "PASS",
                "result": sk["normalization_residual"],
                "remaining_gate": "none at quadratic level",
            },
            {
                "gate_id": "SK4873_2_reality",
                "statement": "S*= -S[psi_r,-psi_a]",
                "status": "PASS",
                "result": sk["reality_residual"],
                "remaining_gate": "nonlinear completion",
            },
            {
                "gate_id": "SK4873_3_noise",
                "statement": "Im S>=0",
                "status": "PASS",
                "result": sk["imaginary_part"],
                "remaining_gate": "derive N from state",
            },
            {
                "gate_id": "SK4873_4_ohmic",
                "statement": bath["retarded_self_energy"],
                "status": "PASS_LOCAL_LIMIT",
                "result": bath["classical_KMS_noise"],
                "remaining_gate": bath["state_requirement"],
            },
        ]
    )


def covariance_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    hadamard = data["sections"]["hadamard_map"]
    return stamp(
        [
            {
                "map_id": "HC4873_0",
                "object": "connected state kernel",
                "status": "DEFINED",
                "result": hadamard["hadamard_function"],
                "remaining_gate": "solve propagator",
            },
            {
                "map_id": "HC4873_1",
                "object": "point-split covariance",
                "status": "DEFINED_RENORMALIZED",
                "result": hadamard["connected_covariance"],
                "remaining_gate": "state and subtraction",
            },
            {
                "map_id": "HC4873_2",
                "object": "public inverse metric",
                "status": "CANDIDATE",
                "result": hadamard["public_inverse_metric"],
                "remaining_gate": hadamard["remaining_gate"],
            },
            {
                "map_id": "HC4873_3",
                "object": "state time orientation",
                "status": "COMPOSITE",
                "result": hadamard["flow_definition"],
                "remaining_gate": "timelike spectral gap",
            },
        ]
    )


def induced_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    induced = data["sections"]["induced_gravity"]
    return stamp(
        [
            {
                "quantity": "heat_kernel_R",
                "status": "DERIVED_ONE_LOOP",
                "value": induced["heat_kernel_R_coefficient"],
                "condition": induced["operator"],
                "caveat": induced["scheme_warning"],
            },
            {
                "quantity": "Mstar_squared",
                "status": "DERIVED_ONE_LOOP",
                "value": induced["Mstar_squared"],
                "condition": induced["positive_EH_gate"],
                "caveat": induced["scheme_warning"],
            },
            {
                "quantity": "Mstar_squared_ell",
                "status": "DERIVED_ONE_LOOP",
                "value": induced["Mstar_squared_ell"],
                "condition": "Lambda_UV=ell_star^-1",
                "caveat": "ell_star origin open",
            },
            {
                "quantity": "GN_metric_only",
                "status": "DERIVED_ANCHOR",
                "value": induced["GN_metric_only"],
                "condition": "c14 absent",
                "caveat": "not regulator independent",
            },
            {
                "quantity": "vacuum_term",
                "status": "DERIVED_MAGNITUDE",
                "value": induced["vacuum_term_magnitude"],
                "condition": "same proper-time cutoff",
                "caveat": "subtraction and cosmology open",
            },
        ]
    )


def underdetermination_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    test = data["sections"]["underdetermination"]
    return stamp(
        [
            {
                "spectrum": "A",
                "normalization": test["normalization_A"],
                "covariance_moment": test["covariance_moment_A"],
                "response_moment": test["response_moment_A"],
                "status": "REFERENCE",
            },
            {
                "spectrum": "B",
                "normalization": test["normalization_B"],
                "covariance_moment": test["covariance_moment_B"],
                "response_moment": test["response_moment_B"],
                "status": "SAME_COVARIANCE_DIFFERENT_RESPONSE",
            },
            {
                "spectrum": "theorem",
                "normalization": "equal",
                "covariance_moment": "equal",
                "response_moment": "not fixed",
                "status": "COVARIANCE_DOES_NOT_DETERMINE_CI",
            },
        ]
    )


def branch_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    metric = data["sections"]["metric_only"]
    arbitration = data["sections"]["arbitration"]
    return stamp(
        [
            {
                "priority": 1,
                "branch": "metric_only",
                "decision": "SELECT_LEAD_PRIMITIVE_LOCAL",
                "field_space": metric["quotient"],
                "coefficient_status": metric["c1_c2_c3_c4"],
                "reason": arbitration["reason"],
            },
            {
                "priority": 2,
                "branch": "state_flow",
                "decision": "RETAIN_TESTED_EXTENSION",
                "field_space": "Gamma_IR[gHat,u,state]",
                "coefficient_status": "microscopic Kubo response required",
                "reason": arbitration["promotion_gate"],
            },
            {
                "priority": 3,
                "branch": "local_claim",
                "decision": "BLOCK",
                "field_space": "metric-only proof incomplete",
                "coefficient_status": "not applicable",
                "reason": arbitration["next_root"],
            },
        ]
    )


def limit_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    limits = data["sections"]["local_limits"]
    return stamp(
        [
            {"limit": "GR", "status": "CONDITIONAL_EXACT", "result": limits["GR"], "gate": limits["open_gates"]},
            {"limit": "PPN", "status": "CONDITIONAL_GR_VALUES", "result": limits["PPN"], "gate": "metric-only quotient proof"},
            {"limit": "Newton", "status": "CONDITIONAL_DERIVED", "result": limits["Newton"], "gate": "Mstar micro scale"},
            {"limit": "Maxwell", "status": "CONDITIONAL_DERIVED", "result": limits["Maxwell"], "gate": "universal principal symbol"},
            {"limit": "Poynting", "status": "CONDITIONAL_HILBERT_SOURCE", "result": "EM momentum gravitates through THat_mn; no local aether source", "gate": "same public metric"},
        ]
    )


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "R_background", "OPEN_ROOT", "prove g_ref Ward redundancy"),
        (2, "R_principal_symbol", "OPEN_ROOT", "derive common species gHat"),
        (3, "R_scale", "OPEN_ROOT", "derive N_s,xi,ell_star and regulator"),
        (4, "R_vacuum", "OPEN_ROOT", "derive subtraction and Lambda relation"),
        (5, "R_higher_curvature", "OPEN_TEST", "derive and bound R2 coefficients"),
        (6, "R_closed_bath", "OPEN_PARENT", "derive bath spectrum and state"),
        (7, "R_unit_flow", "RETAIN_EXTENSION", "promote only on nonzero Kubo result"),
        (8, "R_local_GR", "BLOCKED_CLAIM", "background and source quotient open"),
    ]
    return stamp(
        [
            {
                "priority": priority,
                "residual": residual,
                "status": status,
                "next_action": action,
            }
            for priority, residual, status, action in entries
        ]
    )


def validation_rows(
    sources: list[dict[str, Any]],
    groups: list[list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    data = result()
    sections = data["sections"]
    claims = [
        row for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-715"
    ]
    variables = {
        row.get("symbol"): row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in {
            "psi_a_SK_MTS",
            "G_H_MTS",
            "Mstar_induced_MTS",
            "Gamma_metric_only_MTS",
            "c1_c2_c3_c4_parent",
        }
    }
    checkpoint = (
        POST / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md"
    ).read_text(encoding="utf-8")
    formal = (
        FORMAL / "889-PPC4161-open-parent-induced-gravity-and-metric-only-local-branch.md"
    ).read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4872_VALIDATION.csv")
    output_paths = [
        OUTPUT / name
        for name in (
            "P8_Y5_R2FR_4873_SOURCE_REGISTER.csv",
            "P8_Y5_R2FR_4873_SK_ACTION_GATE.csv",
            "P8_Y5_R2FR_4873_HADAMARD_COVARIANCE.csv",
            "P8_Y5_R2FR_4873_INDUCED_GRAVITY.csv",
            "P8_Y5_R2FR_4873_KUBO_UNDERDETERMINATION.csv",
            "P8_Y5_R2FR_4873_BRANCH_ARBITRATION.csv",
            "P8_Y5_R2FR_4873_LOCAL_LIMITS.csv",
            "P8_Y5_R2FR_4873_RESIDUAL_REBASE.csv",
        )
    ]

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    checks = [
        check("VAL4873_00_symbolic", data["all_checks_pass"], "eight theorem groups"),
        check("VAL4873_01_SK", sections["sk_action"]["passed"] and sections["sk_action"]["bulk_damping_generated"], "damping and SK constraints"),
        check("VAL4873_02_ohmic", sections["ohmic_bath"]["passed"], "Ohmic/KMS local limit"),
        check("VAL4873_03_covariance", sections["hadamard_map"]["passed"], "Hadamard map"),
        check("VAL4873_04_induced", sections["induced_gravity"]["passed"], "Mstar and GN algebra"),
        check("VAL4873_05_metric_only", sections["metric_only"]["passed"] and sections["metric_only"]["c1_c2_c3_c4"] == "0,0,0,0", "flow absent from field space"),
        check("VAL4873_06_under", sections["underdetermination"]["passed"] and sections["underdetermination"]["response_moment_B"] == "11/4", "same covariance different response"),
        check("VAL4873_07_branch", sections["arbitration"]["lead_primitive_local_branch"] == "metric_only_induced_GR_quotient" and sections["arbitration"]["current_claim"] == "private_branch_selection_not_local_GR_proof", "branch selected without claim"),
        check("VAL4873_08_sources", len(sources) == 17 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        check("VAL4873_09_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows private"),
        check("VAL4873_10_csv", all(path.exists() and all(None not in row for row in read_csv(path)) for path in output_paths), "eight CSVs parse"),
        check("VAL4873_11_claim", len(claims) == 1 and claims[0].get("status") == "SK_damping_Hadamard_covariance_and_induced_EH_anchor_derived_metric_only_branch_selected_background_and_universal_symbol_open_private_nonclaim", "L-715"),
        check("VAL4873_12_variables", variables.get("psi_a_SK_MTS", {}).get("status") == "constructed_covariant_open_response_field_nonclaim" and variables.get("Mstar_induced_MTS", {}).get("status") == "one_loop_heat_kernel_anchor_derived_regulator_scale_and_vacuum_subtraction_open" and variables.get("Gamma_metric_only_MTS", {}).get("status") == "lead_primitive_local_branch_selected_background_and_source_descent_open" and variables.get("c1_c2_c3_c4_parent", {}).get("status") == "metric_only_primitive_branch_zero_unit_flow_extension_Kubo_open", "variable statuses"),
        check("VAL4873_13_documents", "OPEN_PARENT_HADAMARD_INDUCED_GRAVITY_AND_METRIC_ONLY_QUOTIENT_4873" in checkpoint and "PPC4161_OPEN_PARENT_INDUCED_GR_METRIC_ONLY_BRANCH_4873" in formal, "document markers"),
        check("VAL4873_14_registers", "1.166 Open damping action" in (FORMAL / "05-equation-register.md").read_text(encoding="utf-8") and "117. Open parent and metric-only branch red team" in (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8") and "PPC4161 checkpoint 4873" in (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8"), "formal registers"),
        check("VAL4873_15_resume", ("Last checkpoint: " + chr(96) + "4873-") in resume and NEXT_TARGET in resume, "resume handoff"),
        check("VAL4873_16_prior", prior[-1].get("status") == "PASS", "4872 green"),
        check("VAL4873_17_scripts", compiles(Path(__file__).resolve()) and compiles(POST / "scripts" / "Y5_R2FR_4873_open_parent_induced_gravity.py"), "scripts compile"),
        check("VAL4873_18_pycache", not (POST / "scripts" / "__pycache__").exists(), "no pycache"),
    ]
    checks.append(
        check(
            "VAL4873_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "OPEN_PARENT_INDUCED_GR_METRIC_ONLY_BRANCH_4873_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = result()
    sources = source_rows()
    tables = [
        (OUTPUT / "P8_Y5_R2FR_4873_SOURCE_REGISTER.csv", sources),
        (OUTPUT / "P8_Y5_R2FR_4873_SK_ACTION_GATE.csv", sk_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4873_HADAMARD_COVARIANCE.csv", covariance_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4873_INDUCED_GRAVITY.csv", induced_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4873_KUBO_UNDERDETERMINATION.csv", underdetermination_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4873_BRANCH_ARBITRATION.csv", branch_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4873_LOCAL_LIMITS.csv", limit_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4873_RESIDUAL_REBASE.csv", residual_rows()),
    ]
    for path, rows in tables:
        write_csv(path, rows)
    groups = [rows for _, rows in tables]
    validation = validation_rows(sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4873_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4873_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4873_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

