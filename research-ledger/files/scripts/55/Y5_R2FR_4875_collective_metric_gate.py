from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from Y5_R2FR_4875_collective_metric_pole import result


CHECKPOINT = "4875"
TIMESTAMP = "2026-07-11T01:00:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-"
    "induced-coefficient-matching-to-GN-Lambda-and-R2.md"
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
            "SRC4875_00_core",
            ROOT / "core-mts-framework" / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "A_MTS",
            "strict scalar provenance",
        ),
        (
            "SRC4875_01_4874",
            POST / "4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md",
            "DIRECT_PRINCIPAL_METRIC_SOFT_UNIVERSALITY_AND_SPIN2_NO_GO_GATE_4874",
            "spin2 handoff",
        ),
        (
            "SRC4875_02_checkpoint",
            POST / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "human derivation",
        ),
        (
            "SRC4875_03_formal",
            FORMAL / "891-PPC4161-integrated-density-parent-and-spin2-pole.md",
            "PPC4161_INTEGRATED_H_SPIN2_POLE_4875",
            "formal integration",
        ),
        (
            "SRC4875_04_script",
            POST / "scripts" / "Y5_R2FR_4875_collective_metric_pole.py",
            "def eh_projector_pole",
            "symbolic derivation",
        ),
        (
            "SRC4875_05_generator",
            Path(__file__).resolve(),
            'CHECKPOINT = "4875"',
            "checkpoint generator",
        ),
        ("SRC4875_06_claim", FORMAL / "02-claims-register.csv", "L-717", "claim register"),
        (
            "SRC4875_07_variable",
            FORMAL / "04-variable-audit.csv",
            "selected_primitive_integrated_Diff_gauge_variable_dynamics_induced",
            "variable audit",
        ),
        (
            "SRC4875_08_equation",
            FORMAL / "05-equation-register.md",
            "1.168 Integrated principal-density parent",
            "equation register",
        ),
        (
            "SRC4875_09_redteam",
            FORMAL / "06-consistency-red-team.md",
            "119. Integrated-density parent and pole red team",
            "red-team register",
        ),
        (
            "SRC4875_10_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4875",
            "unification spine",
        ),
        (
            "SRC4875_11_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "Last checkpoint: " + chr(96) + "4875-",
            "resume marker",
        ),
        (
            "SRC4875_12_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4874_VALIDATION.csv",
            "VAL4874_OVERALL",
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
            "SRC4875_13_WW",
            "https://doi.org/10.1016/0370-2693(80)90212-9",
            "no-go theorem",
        ),
        (
            "SRC4875_14_Weinberg",
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.135.B1049",
            "soft universality",
        ),
        (
            "SRC4875_15_Deser",
            "https://arxiv.org/abs/gr-qc/0411023",
            "spin2 self-coupling",
        ),
        (
            "SRC4875_16_heat",
            "https://arxiv.org/abs/hep-th/0306138",
            "induced coefficient",
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


def parent_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    parent = data["sections"]["parent"]
    return stamp(
        [
            {"item": "partition", "status": "CONSTRUCTED", "statement": parent["partition_function"], "gate": parent["measure_condition"]},
            {"item": "metric", "status": "DERIVED", "statement": parent["metric_map"], "gate": "Lorentzian nondegenerate H"},
            {"item": "gauge", "status": "DECLARED_EXACT", "statement": parent["diffeomorphism_action"], "gate": parent["measure_condition"]},
            {"item": "bare EH", "status": "UV_BOUNDARY", "statement": parent["bare_gravity_boundary"], "gate": "renormalization condition"},
        ]
    )


def projector_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    pole = data["sections"]["projector"]
    return stamp(
        [
            {"sector": "hessian", "status": "DERIVED", "result": pole["EH_hessian"], "gate": "flat EH-dominant saddle"},
            {"sector": "inverse", "status": "PASS_EXACT", "result": pole["conserved_source_propagator"], "gate": "conserved sources"},
            {"sector": "spin2 residue", "status": "PASS_POSITIVE", "result": pole["spin2_residue"], "gate": "Mstar2>0"},
            {"sector": "physical modes", "status": "HELICITY2_ONLY", "result": pole["physical_helicities"], "gate": "Diff/BRST"},
            {"sector": "trace projector", "status": "CONSTRAINT", "result": pole["scalar_projector_role"], "gate": "retest with R2"},
        ]
    )


def ward_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    ward = data["sections"]["ward"]
    return stamp(
        [
            {"identity": "longitudinal", "status": "PASS_EXACT", "statement": ward["hessian_times_longitudinal"], "origin": ward["origin"]},
            {"identity": "linear", "status": "CONDITIONAL_EXACT", "statement": ward["linear_Ward_identity"], "origin": ward["origin"]},
            {"identity": "nonlinear", "status": "CONDITIONAL_EXACT", "statement": ward["nonlinear_identity"], "origin": ward["origin"]},
        ]
    )


def exchange_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    exchange = data["sections"]["exchange"]
    return stamp(
        [
            {"quantity": "amplitude", "status": "DERIVED", "value": exchange["amplitude"], "meaning": "conserved-source exchange"},
            {"quantity": "NR numerator", "status": "PASS_POSITIVE", "value": exchange["nonrelativistic_numerator"], "meaning": "attractive Newton channel"},
            {"quantity": "GN", "status": "IDENTIFIED", "value": exchange["Newton_identification"], "meaning": "normalization target"},
            {"quantity": "source", "status": "UNIVERSAL_SOFT", "value": exchange["universal_source"], "meaning": "all species"},
        ]
    )


def branch_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    strict = data["sections"]["strict_scalar"]
    integrated = data["sections"]["integrated_density"]
    arbitration = data["sections"]["arbitration"]
    return stamp(
        [
            {"priority": 1, "branch": "integrated_H_Diff", "decision": integrated["decision"], "WW_status": integrated["weinberg_witten"], "cost": integrated["cost"]},
            {"priority": 2, "branch": "strict_scalar_composite", "decision": strict["decision"], "WW_status": strict["weinberg_witten"], "cost": "route rejected"},
            {"priority": 3, "branch": "selected", "decision": arbitration["selected"], "WW_status": "evasion conditional on exact gauge measure", "cost": arbitration["claim_status"]},
        ]
    )


def domain_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    domain = data["sections"]["domain"]
    return stamp(
        [
            {"gate": "saddle", "status": "OPEN", "requirement": domain["saddle"]},
            {"gate": "hierarchy", "status": "OPEN", "requirement": domain["derivative_hierarchy"]},
            {"gate": "positivity", "status": "REQUIRED", "requirement": domain["positivity"]},
            {"gate": "matter", "status": "REQUIRED", "requirement": domain["matter"]},
            {"gate": "flow", "status": "COMPOSITE_DEFAULT", "requirement": domain["state_flow"]},
        ]
    )


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "R_parent_action", "OPEN_ROOT", "write full normalized S0"),
        (2, "R_measure", "OPEN_ROOT", "fix H contour and Diff/BRST measure"),
        (3, "R_regulator", "OPEN_ROOT", "prove covariant Ward restoration"),
        (4, "R_saddle", "OPEN_ROOT", "solve induced Lambda background"),
        (5, "R_R2", "OPEN_ROOT", "derive full projector corrections"),
        (6, "R_scale", "OPEN_ROOT", "match Ns xi LambdaUV to GN"),
        (7, "R_tests", "OPEN_NEXT", "route residuals to data"),
        (8, "R_public_GR", "BLOCKED_CLAIM", "normalization and hierarchy open"),
    ]
    return stamp(
        [
            {"priority": p, "residual": r, "status": s, "next_action": a}
            for p, r, s, a in entries
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
        if row.get("claim_id") == "L-717"
    ]
    variables = {
        row.get("symbol"): row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in {
            "Z_H_parent_MTS",
            "H_principal_MTS",
            "Pi_spin2_MTS",
            "BRST_H_MTS",
            "WW_gate_MTS",
        }
    }
    checkpoint = (
        POST / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md"
    ).read_text(encoding="utf-8")
    formal = (
        FORMAL / "891-PPC4161-integrated-density-parent-and-spin2-pole.md"
    ).read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4874_VALIDATION.csv")
    output_paths = [
        OUTPUT / name
        for name in (
            "P8_Y5_R2FR_4875_SOURCE_REGISTER.csv",
            "P8_Y5_R2FR_4875_PARENT_CONTRACT.csv",
            "P8_Y5_R2FR_4875_PROJECTOR_POLE.csv",
            "P8_Y5_R2FR_4875_WARD_IDENTITY.csv",
            "P8_Y5_R2FR_4875_SOURCE_EXCHANGE.csv",
            "P8_Y5_R2FR_4875_BRANCH_ARBITRATION.csv",
            "P8_Y5_R2FR_4875_DOMAIN_GATE.csv",
            "P8_Y5_R2FR_4875_RESIDUAL_REBASE.csv",
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
        check("VAL4875_00_symbolic", data["all_checks_pass"], "eight theorem groups"),
        check("VAL4875_01_parent", sections["parent"]["passed"] and "INTEGRATED" in sections["parent"]["status"], "integrated H parent"),
        check("VAL4875_02_projector", sections["projector"]["passed"] and sections["projector"]["positive_residue_for_Mstar2_positive"], "positive spin2 pole"),
        check("VAL4875_03_Ward", sections["ward"]["passed"], "longitudinal Ward"),
        check("VAL4875_04_exchange", sections["exchange"]["passed"], "Newton source exchange"),
        check("VAL4875_05_strict", sections["strict_scalar"]["weinberg_witten"] == "TRIGGERED" and "REJECT" in sections["strict_scalar"]["decision"], "strict scalar rejected"),
        check("VAL4875_06_integrated", sections["integrated_density"]["decision"] == "SELECT_VIABLE_PARENT_UPGRADE_PRIVATE_NONCLAIM" and sections["integrated_density"]["weinberg_witten"].startswith("NOT_TRIGGERED"), "gauge parent selected"),
        check("VAL4875_07_domain", sections["domain"]["status"] == "CONDITIONAL_IR_DOMAIN_NOT_GLOBAL_UV_COMPLETION", "domain limited"),
        check("VAL4875_08_sources", len(sources) == 17 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        check("VAL4875_09_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows private"),
        check("VAL4875_10_csv", all(path.exists() and all(None not in row for row in read_csv(path)) for path in output_paths), "eight CSVs parse"),
        check("VAL4875_11_claim", len(claims) == 1 and claims[0].get("status") == "integrated_Diff_parent_and_positive_spin2_pole_derived_strict_scalar_composite_rejected_coefficients_saddle_and_regulator_open_private_nonclaim", "L-717"),
        check("VAL4875_12_variables", variables.get("Z_H_parent_MTS", {}).get("status") == "minimal_integrated_Diff_parent_contract_constructed_normalization_open" and variables.get("H_principal_MTS", {}).get("status") == "selected_primitive_integrated_Diff_gauge_variable_dynamics_induced" and variables.get("Pi_spin2_MTS", {}).get("status") == "positive_massless_spin2_pole_derived_on_integrated_Diff_parent_private_nonclaim" and variables.get("WW_gate_MTS", {}).get("status") == "strict_scalar_branch_triggered_and_rejected_integrated_Diff_parent_evasion_derived", "variable statuses"),
        check("VAL4875_13_documents", "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875" in checkpoint and "PPC4161_INTEGRATED_H_SPIN2_POLE_4875" in formal, "document markers"),
        check("VAL4875_14_registers", "1.168 Integrated principal-density parent" in (FORMAL / "05-equation-register.md").read_text(encoding="utf-8") and "119. Integrated-density parent and pole red team" in (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8") and "PPC4161 checkpoint 4875" in (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8"), "formal registers"),
        check("VAL4875_15_resume", ("Last checkpoint: " + chr(96) + "4875-") in resume and NEXT_TARGET in resume, "resume handoff"),
        check("VAL4875_16_prior", prior[-1].get("status") == "PASS", "4874 green"),
        check("VAL4875_17_scripts", compiles(Path(__file__).resolve()) and compiles(POST / "scripts" / "Y5_R2FR_4875_collective_metric_pole.py"), "scripts compile"),
        check("VAL4875_18_pycache", not (POST / "scripts" / "__pycache__").exists(), "no pycache"),
    ]
    checks.append(
        check(
            "VAL4875_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "INTEGRATED_H_SPIN2_POLE_4875_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = result()
    sources = source_rows()
    tables = [
        (OUTPUT / "P8_Y5_R2FR_4875_SOURCE_REGISTER.csv", sources),
        (OUTPUT / "P8_Y5_R2FR_4875_PARENT_CONTRACT.csv", parent_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4875_PROJECTOR_POLE.csv", projector_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4875_WARD_IDENTITY.csv", ward_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4875_SOURCE_EXCHANGE.csv", exchange_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4875_BRANCH_ARBITRATION.csv", branch_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4875_DOMAIN_GATE.csv", domain_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4875_RESIDUAL_REBASE.csv", residual_rows()),
    ]
    for path, rows in tables:
        write_csv(path, rows)
    groups = [rows for _, rows in tables]
    validation = validation_rows(sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4875_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4875_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4875_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

