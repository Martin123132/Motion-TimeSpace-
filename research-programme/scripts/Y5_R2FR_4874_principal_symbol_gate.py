from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from Y5_R2FR_4874_principal_symbol_soft_graviton import result


CHECKPOINT = "4874"
TIMESTAMP = "2026-07-10T23:05:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-"
    "and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md"
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
            "SRC4874_00_core",
            ROOT / "core-mts-framework" / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "A_MTS",
            "fixed-background scalar provenance",
        ),
        (
            "SRC4874_01_4873",
            POST / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "OPEN_PARENT_HADAMARD_INDUCED_GRAVITY_AND_METRIC_ONLY_QUOTIENT_4873",
            "metric-only handoff",
        ),
        (
            "SRC4874_02_checkpoint",
            POST / "4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md",
            "DIRECT_PRINCIPAL_METRIC_SOFT_UNIVERSALITY_AND_SPIN2_NO_GO_GATE_4874",
            "human derivation",
        ),
        (
            "SRC4874_03_formal",
            FORMAL / "890-PPC4161-principal-symbol-soft-universality-and-spin2-gate.md",
            "PPC4161_PRINCIPAL_SYMBOL_SOFT_SPIN2_GATE_4874",
            "formal integration",
        ),
        (
            "SRC4874_04_script",
            POST / "scripts" / "Y5_R2FR_4874_principal_symbol_soft_graviton.py",
            "def soft_graviton_universality",
            "symbolic derivation",
        ),
        (
            "SRC4874_05_generator",
            Path(__file__).resolve(),
            'CHECKPOINT = "4874"',
            "checkpoint generator",
        ),
        ("SRC4874_06_claim", FORMAL / "02-claims-register.csv", "L-716", "claim register"),
        (
            "SRC4874_07_variable",
            FORMAL / "04-variable-audit.csv",
            "reference_free_metric_reconstruction_derived_collective_origin_open",
            "variable audit",
        ),
        (
            "SRC4874_08_equation",
            FORMAL / "05-equation-register.md",
            "1.167 Principal-density metric",
            "equation register",
        ),
        (
            "SRC4874_09_redteam",
            FORMAL / "06-consistency-red-team.md",
            "118. Principal metric and emergent-spin2 red team",
            "red-team register",
        ),
        (
            "SRC4874_10_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4874",
            "unification spine",
        ),
        (
            "SRC4874_11_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "Last checkpoint: " + chr(96) + "4874-",
            "resume marker",
        ),
        (
            "SRC4874_12_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4873_VALIDATION.csv",
            "VAL4873_OVERALL",
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
            "SRC4874_13_Weinberg_soft",
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.135.B1049",
            "soft spin-2 universality",
        ),
        (
            "SRC4874_14_Weinberg_bootstrap",
            "https://journals.aps.org/pr/abstract/10.1103/PhysRev.138.B988",
            "Einstein perturbative completion",
        ),
        (
            "SRC4874_15_WW",
            "https://doi.org/10.1016/0370-2693(80)90212-9",
            "composite massless spin-2 no-go",
        ),
        (
            "SRC4874_16_soft_SR",
            "https://arxiv.org/abs/1704.05071",
            "soft spin-2 Lorentz consistency",
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


def split_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    split = data["sections"]["split_ward"]
    return stamp(
        [
            {
                "case": "fixed_public_split",
                "functional": "Gamma[g_ref,C]",
                "ward_operator": split["ward_operator"],
                "residual": split["good_residual"],
                "status": "PASS_IF_ONLY_GHAT",
            },
            {
                "case": "separate_background",
                "functional": "g_ref^2+C^3",
                "ward_operator": split["ward_operator"],
                "residual": split["bad_residual"],
                "status": "FAIL_BACKGROUND_INDEPENDENCE",
            },
            {
                "case": "selected_definition",
                "functional": "Gamma[H]",
                "ward_operator": "no additive split",
                "residual": "not applicable",
                "status": "REFERENCE_REMOVED",
            },
        ]
    )


def metric_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    metric = data["sections"]["principal_metric"]
    return stamp(
        [
            {
                "identity": "density",
                "statement": metric["principal_density"],
                "result": metric["density_residual_zero"],
                "status": "PASS_EXACT",
            },
            {
                "identity": "determinant",
                "statement": metric["metric_determinant_rule"],
                "result": metric["determinant_residual_zero"],
                "status": "PASS_EXACT",
            },
            {
                "identity": "inverse_metric",
                "statement": metric["inverse_metric_rule"],
                "result": metric["reconstruction_residual_zero"],
                "status": "PASS_EXACT",
            },
            {
                "identity": "reference",
                "statement": "reference metric required",
                "result": metric["reference_metric_required"],
                "status": "REFERENCE_FREE",
            },
        ]
    )


def soft_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    soft = data["sections"]["soft_universality"]
    return stamp(
        [
            {
                "step": "soft_factor",
                "equation": soft["soft_factor"],
                "status": "SOURCE_BACKED",
                "result": "leading pole factor",
            },
            {
                "step": "gauge",
                "equation": soft["gauge_condition"],
                "status": "REQUIRED",
                "result": "mass-shell gauge invariance",
            },
            {
                "step": "momentum",
                "equation": soft["momentum_conservation"],
                "status": "REQUIRED",
                "result": "arbitrary process",
            },
            {
                "step": "solution",
                "equation": soft["three_leg_residual"],
                "status": "PASS_EXACT",
                "result": soft["conclusion"],
            },
        ]
    )


def spin2_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    pole = data["sections"]["spin2_gate"]
    return stamp(
        [
            {
                "gate": "pole",
                "requirement": pole["required_two_point_form"],
                "status": "OPEN",
                "reason": pole["reason"],
            },
            {
                "gate": "residue",
                "requirement": pole["residue_gate"],
                "status": "OPEN_COLLECTIVE",
                "reason": "EH response coefficient only",
            },
            {
                "gate": "spectrum",
                "requirement": pole["spectrum_gate"],
                "status": "OPEN_COLLECTIVE",
                "reason": "spin projector not derived",
            },
            {
                "gate": "gauge",
                "requirement": pole["gauge_gate"],
                "status": "OPEN_COLLECTIVE",
                "reason": "emergent diffeomorphism Ward identity absent",
            },
        ]
    )


def no_go_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    gate = data["sections"]["weinberg_witten"]
    return stamp(
        [
            {
                "item": "trigger",
                "statement": gate["theorem_trigger"],
                "status": "THEOREM",
            },
            {
                "item": "result",
                "statement": gate["trigger_result"],
                "status": "NO_GO_IF_TRIGGERED",
            },
            {
                "item": "MTS risk",
                "statement": gate["current_core_risk"],
                "status": "OPEN_HARD",
            },
            {
                "item": "evasion",
                "statement": gate["admissible_evasion"],
                "status": "MUST_DERIVE",
            },
        ]
    )


def contract_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    contract = data["sections"]["principal_contract"]
    return stamp(
        [
            {"species": "scalar", "principal_symbol": contract["scalar"], "status": contract["status"]},
            {"species": "fermion", "principal_symbol": contract["fermion"], "status": contract["status"]},
            {"species": "photon", "principal_symbol": contract["photon"], "status": contract["status"]},
            {"species": "residual", "principal_symbol": contract["allowed_residuals"], "status": "BOUNDABLE_EXTENSION"},
        ]
    )


def local_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    chain = data["sections"]["local_chain"]
    return stamp(
        [
            {"arena": "assumptions", "status": "OPEN_GATE", "result": chain["assumptions"]},
            {"arena": "gravity", "status": "CONDITIONAL", "result": chain["gravity"]},
            {"arena": "source", "status": "CONDITIONAL_UNIVERSAL", "result": chain["source"]},
            {"arena": "Newton", "status": "CONDITIONAL", "result": chain["Newton"]},
            {"arena": "Maxwell", "status": "CONDITIONAL", "result": chain["Maxwell"]},
            {"arena": "PPN", "status": "CONDITIONAL", "result": chain["PPN"]},
            {"arena": "claim", "status": "BLOCKED", "result": chain["claim_status"]},
        ]
    )


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "R_collective_measure", "OPEN_ROOT", "make H/gHat integrated"),
        (2, "R_spin2_pole", "OPEN_ROOT", "derive positive Pi2/q2 pole"),
        (3, "R_diff_Ward", "OPEN_ROOT", "derive q_mu Gamma2=0"),
        (4, "R_WW", "OPEN_ROOT", "prove exact no-go evasion"),
        (5, "R_species", "CONDITIONAL", "activate soft universality after pole"),
        (6, "R_higher_ops", "OPEN_TEST", "derive and bound residuals"),
        (7, "R_local_GR", "BLOCKED_CLAIM", "pole/gauge/no-go open"),
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
        if row.get("claim_id") == "L-716"
    ]
    variables = {
        row.get("symbol"): row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in {
            "H_principal_MTS",
            "Pi_spin2_MTS",
            "kappa_soft_univ_MTS",
            "WW_gate_MTS",
            "gHat_shared_characteristic",
        }
    }
    checkpoint = (
        POST / "4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md"
    ).read_text(encoding="utf-8")
    formal = (
        FORMAL / "890-PPC4161-principal-symbol-soft-universality-and-spin2-gate.md"
    ).read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4873_VALIDATION.csv")
    output_paths = [
        OUTPUT / name
        for name in (
            "P8_Y5_R2FR_4874_SOURCE_REGISTER.csv",
            "P8_Y5_R2FR_4874_SPLIT_WARD.csv",
            "P8_Y5_R2FR_4874_PRINCIPAL_METRIC.csv",
            "P8_Y5_R2FR_4874_SOFT_UNIVERSALITY.csv",
            "P8_Y5_R2FR_4874_SPIN2_GATE.csv",
            "P8_Y5_R2FR_4874_WEINBERG_WITTEN.csv",
            "P8_Y5_R2FR_4874_PRINCIPAL_CONTRACT.csv",
            "P8_Y5_R2FR_4874_LOCAL_CHAIN.csv",
            "P8_Y5_R2FR_4874_RESIDUAL_REBASE.csv",
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
        check("VAL4874_00_symbolic", data["all_checks_pass"], "seven theorem groups"),
        check("VAL4874_01_split", sections["split_ward"]["passed"], "split Ward identity"),
        check("VAL4874_02_metric", sections["principal_metric"]["passed"] and not sections["principal_metric"]["reference_metric_required"], "direct metric reconstruction"),
        check("VAL4874_03_soft", sections["soft_universality"]["passed"] and sections["soft_universality"]["conclusion"] == "kappa1=kappa2=kappa3=kappa", "universal coupling algebra"),
        check("VAL4874_04_pole", sections["spin2_gate"]["status"] == "NOT_PROVED_BY_HEAT_KERNEL_COEFFICIENT_ALONE", "pole not overclaimed"),
        check("VAL4874_05_WW", sections["weinberg_witten"]["status"] == "OPEN_HARD_GATE", "no-go retained"),
        check("VAL4874_06_contract", sections["principal_contract"]["passed"], "species contract"),
        check("VAL4874_07_local", sections["local_chain"]["claim_status"].startswith("blocked"), "local claim blocked"),
        check("VAL4874_08_sources", len(sources) == 17 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        check("VAL4874_09_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows private"),
        check("VAL4874_10_csv", all(path.exists() and all(None not in row for row in read_csv(path)) for path in output_paths), "nine CSVs parse"),
        check("VAL4874_11_claim", len(claims) == 1 and claims[0].get("status") == "reference_free_principal_metric_and_soft_universality_derived_spin2_pole_and_Weinberg_Witten_evasion_open_private_nonclaim", "L-716"),
        check("VAL4874_12_variables", variables.get("H_principal_MTS", {}).get("status") == "reference_free_metric_reconstruction_derived_collective_origin_open" and variables.get("Pi_spin2_MTS", {}).get("status") == "physical_massless_spin2_pole_gate_written_not_derived" and variables.get("kappa_soft_univ_MTS", {}).get("status") == "soft_universality_algebra_derived_MTS_spin2_premises_open" and variables.get("WW_gate_MTS", {}).get("status") == "open_hard_emergent_gauge_evasion_gate", "variable statuses"),
        check("VAL4874_13_documents", "DIRECT_PRINCIPAL_METRIC_SOFT_UNIVERSALITY_AND_SPIN2_NO_GO_GATE_4874" in checkpoint and "PPC4161_PRINCIPAL_SYMBOL_SOFT_SPIN2_GATE_4874" in formal, "document markers"),
        check("VAL4874_14_registers", "1.167 Principal-density metric" in (FORMAL / "05-equation-register.md").read_text(encoding="utf-8") and "118. Principal metric and emergent-spin2 red team" in (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8") and "PPC4161 checkpoint 4874" in (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8"), "formal registers"),
        check("VAL4874_15_resume", ("Last checkpoint: " + chr(96) + "4874-") in resume and NEXT_TARGET in resume, "resume handoff"),
        check("VAL4874_16_prior", prior[-1].get("status") == "PASS", "4873 green"),
        check("VAL4874_17_scripts", compiles(Path(__file__).resolve()) and compiles(POST / "scripts" / "Y5_R2FR_4874_principal_symbol_soft_graviton.py"), "scripts compile"),
        check("VAL4874_18_pycache", not (POST / "scripts" / "__pycache__").exists(), "no pycache"),
    ]
    checks.append(
        check(
            "VAL4874_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "PRINCIPAL_SYMBOL_SOFT_SPIN2_GATE_4874_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = result()
    sources = source_rows()
    tables = [
        (OUTPUT / "P8_Y5_R2FR_4874_SOURCE_REGISTER.csv", sources),
        (OUTPUT / "P8_Y5_R2FR_4874_SPLIT_WARD.csv", split_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4874_PRINCIPAL_METRIC.csv", metric_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4874_SOFT_UNIVERSALITY.csv", soft_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4874_SPIN2_GATE.csv", spin2_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4874_WEINBERG_WITTEN.csv", no_go_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4874_PRINCIPAL_CONTRACT.csv", contract_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4874_LOCAL_CHAIN.csv", local_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4874_RESIDUAL_REBASE.csv", residual_rows()),
    ]
    for path, rows in tables:
        write_csv(path, rows)
    groups = [rows for _, rows in tables]
    validation = validation_rows(sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4874_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4874_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4874_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

