from __future__ import annotations

import csv
import math
import tarfile
from pathlib import Path
from typing import Any

import sympy as sp

from Y5_R2FR_4871_asymptotic_surface_identity import surface_identity
from Y5_R2FR_4871_C3_source_arbitration import (
    arbitration,
    external_decomposition,
    parent_parity_rows,
    source_audit,
)


CHECKPOINT = "4871"
TIMESTAMP = "2026-07-10T17:05:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-"
    "source-coupling-or-correspondence-demotion.md"
)
GRID_PATH = OUTPUT / "P8_Y5_R2FR_4871_V3_ASYMPTOTIC_RESPONSE.csv"


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


def archive_contains(path: Path, member: str, needle: str) -> bool:
    if not path.exists():
        return False
    try:
        with tarfile.open(path, "r:*") as archive:
            extracted = archive.extractfile(member)
            if extracted is None:
                return False
            return needle in extracted.read().decode("utf-8", errors="replace")
    except (tarfile.TarError, OSError):
        return False


def resume_checkpoint_at_least(resume: str, checkpoint: int) -> bool:
    prefix = "Last checkpoint: " + chr(96)
    for line in resume.splitlines():
        if line.startswith(prefix):
            token = line[len(prefix) :].split("-", 1)[0]
            return token.isdigit() and int(token) >= checkpoint
    return False


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4871_00_prior_checkpoint", POST / "4870-Y5-R2FR-v4-stationary-mass-identity-and-finite-compactness-parent-kappa4-or-v3-tail-crosscheck.md", "V4_STATIONARY_MASS_IDENTITY_4870", "stationary-mass parent result"),
        ("SRC4871_01_prior_formal", FORMAL / "886-PPC4161-v4-stationary-mass-and-finite-C-parent-response.md", "PPC4161_V4_STATIONARY_MASS_4870", "prior formal integration"),
        ("SRC4871_02_prior_validation", OUTPUT / "P8_Y5_BRR545_4870_VALIDATION.csv", "VAL4870_OVERALL", "prior validation"),
        ("SRC4871_03_checkpoint", POST / "4871-Y5-R2FR-v3-l1-asymptotic-kappa4-crosscheck-and-full-first-order-C3-arbitration.md", "V3_L1_SURFACE_KAPPA4_AND_C3_ARBITRATION_4871", "human derivation"),
        ("SRC4871_04_formal", FORMAL / "887-PPC4161-v3-tail-kappa4-and-C3-arbitration.md", "PPC4161_V3_TAIL_KAPPA4_C3_ARBITRATION_4871", "formal integration"),
        ("SRC4871_05_claim", FORMAL / "02-claims-register.csv", "L-713", "claim register"),
        ("SRC4871_06_q3_variable", FORMAL / "04-variable-audit.csv", "derived_finite_C_parent_profile_asymptotic_kappa4_crosscheck_nonclaim", "q3 variable"),
        ("SRC4871_07_kappa_variable", FORMAL / "04-variable-audit.csv", "finite_C_parent_response_derived_v3_surface_crosschecked_binary_safe_primitive_ownership_open_nonclaim", "kappa variable"),
        ("SRC4871_08_s_variable", FORMAL / "04-variable-audit.csv", "finite_C_parent_correspondence_response_derived_C3_internal_selected_external_source_discrepancy_nonclaim", "first-response variable"),
        ("SRC4871_09_equation", FORMAL / "05-equation-register.md", "1.164 Third-order dipole equation", "equation register"),
        ("SRC4871_10_redteam", FORMAL / "06-consistency-red-team.md", "115. Third-order tail and C3 arbitration red team", "red-team register"),
        ("SRC4871_11_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4871", "unification spine"),
        ("SRC4871_12_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: " + chr(96) + "4871-", "resume marker"),
        ("SRC4871_13_v3_script", POST / "scripts" / "Y5_R2FR_4871_v3_asymptotic_response.py", "numeric_v3_source", "third-order Euler source and BVP"),
        ("SRC4871_14_surface_script", POST / "scripts" / "Y5_R2FR_4871_asymptotic_surface_identity.py", "surface_identity", "asymptotic current derivation"),
        ("SRC4871_15_grid_script", POST / "scripts" / "Y5_R2FR_4871_v3_grid_runner.py", "surface_responses", "finite-C tail grid"),
        ("SRC4871_16_C3_script", POST / "scripts" / "Y5_R2FR_4871_C3_source_arbitration.py", "external_decomposition", "C3 source arbitration"),
        ("SRC4871_17_generator", Path(__file__).resolve(), 'CHECKPOINT = "4871"', "checkpoint generator"),
        ("SRC4871_18_grid", GRID_PATH, "V3_4871_C0.300_r0.33333333", "executed finite-C response rows"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "member": "",
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": needle in content,
                "role": role,
                "source_validated": path.exists() and needle in content,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    archives = [
        ("SRC4871_19_yagi", Path(r"D:\Temp\1311.7144-source.tar"), "paper.tex", r"\label{ae:mass}", "stationary surface variation"),
        ("SRC4871_20_gupta_v1", Path(r"D:\Temp\2104.04596v1-source.tar"), "main.tex", r"\label{tolman_sens_C}", "arXiv v1 C3 source"),
        ("SRC4871_21_gupta_v2", Path(r"D:\Temp\2104.04596-source.tar"), "main.tex", r"\label{tolman_sens_C}", "arXiv v2 C3 source"),
    ]
    for source_id, path, member, needle, role in archives:
        valid = archive_contains(path, member, needle)
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local_primary_archive",
                "source_locator": str(path),
                "member": member,
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": valid,
                "role": role,
                "source_validated": valid,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4871_22_urls",
            "source_kind": "primary_url_ledger",
            "source_locator": "https://arxiv.org/abs/1311.7144;https://arxiv.org/abs/2104.04596;https://arxiv.org/abs/gr-qc/0509121",
            "member": "",
            "needle": "primary URLs recorded",
            "source_exists": True,
            "needle_found": True,
            "role": "primary provenance ledger",
            "source_validated": True,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def v3_equation_rows() -> list[dict[str, Any]]:
    entries = [
        ("V3EQ4871_00_hierarchy", "normalized flow hierarchy", "q=q1+v2*q3+O(v4)", "exact gamma*v asymptotic factor removed", "DERIVED_PARENT"),
        ("V3EQ4871_01_action", "reduced action hierarchy", "Iae_bar=v2*I2[q]+v4*I4[q]+O(v6)", "same parent L2/L4 functionals as checkpoint 4868", "DERIVED_PARENT"),
        ("V3EQ4871_02_equation", "third-order dipole equation", "H2[q1]*q3=-E4[q1]", "inhomogeneous equation without fitted coefficient", "DERIVED_PARENT"),
        ("V3EQ4871_03_center", "center boundary", "a3(0)=b3(0);a3_prime(0)=0", "regular l1 profile", "DERIVED_PARENT"),
        ("V3EQ4871_04_infinity", "outer boundary", "R*a3_prime+a3=R*b3_prime+b3=0", "decaying 1/R residual tail", "DERIVED_PARENT"),
        ("V3EQ4871_05_stationarity", "first variation", "delta_I2[q1;q3]=0", "five-row extrapolated magnitude below 5.6e-8", "NUMERIC_CROSSCHECK"),
        ("V3EQ4871_06_ownership", "scope", "selected correspondence action at O(p)", "primitive MTS ownership remains open", "PRIVATE_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "derived": derived,
            "expected_or_role": expected,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, derived, expected, status in entries
    ]


def surface_rows() -> list[dict[str, Any]]:
    identities = surface_identity()
    return [
        {
            "row_id": f"SURF4871_{index:02d}",
            "quantity": key,
            "expression": sp.sstr(value),
            "status": "DERIVED_EXACT",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for index, (key, value) in enumerate(identities.items())
    ]


def with_metadata(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row in rows
    ]


def arbitration_rows() -> list[dict[str, Any]]:
    values = arbitration()
    return [
        {
            "row_id": f"ARB4871_{index:02d}",
            "quantity": key,
            "value": value,
            "status": (
                "INTERNAL_PARENT_SELECTED"
                if key == "decision"
                else "AUDITED"
            ),
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for index, (key, value) in enumerate(values.items())
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "v3 l1 parent equation", "CLOSED_DERIVED", "H2 q3=-E4 with regular and decaying boundary data"),
        (2, "quartic surface current", "CLOSED_EXACT", "normalization reproduces the exact first-response Ward map"),
        (3, "finite-C kappa4 cross-check", "PASS", "five action-surface gaps below 1.83e-8"),
        (4, "D4 completion", "DERIVED_NOT_FREE_CONFIRMED", "independent asymptotic response reproduces stationary-mass kappa4"),
        (5, "parent C3", "SELECT_INTERNAL", "refined a3=4.9573884 and exact a2 regression"),
        (6, "printed Gupta C3", "DEMOTE_EXTERNAL_SOURCE_DISCREPANCY", "disjoint and syntactically incomplete; no author code"),
        (7, "external-paper correction", "NOT_CLAIMED", "source discrepancy is not an erratum"),
        (8, "compact-response ladder", "STOP_EXTENDING", "internal parent response has four mutually consistent readouts"),
        (9, "primitive MTS ownership", "OPEN_HARD_NEXT", "correspondence action and universal source metric remain underived"),
        (10, "next derivation", "PRIMITIVE_ACTION_AND_SOURCE_COUPLING", NEXT_TARGET),
    ]
    return [
        {
            "priority": priority,
            "target": target,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, target, decision, reason in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "R_v3_l1_equation", "CLOSED_PARENT", "exact generated Euler source", "retain as primitive-bridge regression"),
        (2, "R_v3_tail", "CLOSED_NUMERIC", "five finite-C BVP rows", "repeat on tabulated EoSs later"),
        (3, "R_kappa4_surface", "CLOSED_EXACT_NUMERIC", "exact current plus 1.83e-8 grid agreement", "do not fit a completion"),
        (4, "R_D4", "CLOSED_DERIVED_PARTITION", "surface response confirms stationary mass", "do not reopen"),
        (5, "R_parent_C3", "CLOSED_INTERNAL_BRANCH", "4.95<a3<4.97 and a2 regression", "use parent branch internally"),
        (6, "R_external_C3", "OPEN_LITERATURE_SOURCE", "printed formula disjoint and syntactically incomplete", "seek author derivation only before public comparison"),
        (7, "R_EOS", "OPEN_EXTENSION", "Tolman VII sampled only", "repeat after primitive ownership"),
        (8, "R_solitary_map", "OPEN_EXTENSION", "binary map is not one-body spin map", "derive after primitive ownership"),
        (9, "R_primitive_action", "OPEN_HARD_NEXT", "unit-flow action not derived from primitive MTS variables", "checkpoint 4872"),
        (10, "R_local_GR", "OPEN_HARD", "primitive coupling and ownership remain missing", "do not promote"),
    ]
    return [
        {
            "priority": priority,
            "residual": residual,
            "status": status,
            "evidence": evidence,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, residual, status, evidence, next_action in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    equations: list[dict[str, Any]],
    surfaces: list[dict[str, Any]],
    grid: list[dict[str, str]],
    source_c3: list[dict[str, Any]],
    parity: list[dict[str, Any]],
    decomposition: list[dict[str, Any]],
    arbitration_data: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    identities = surface_identity()
    symbol_map = {
        symbol.name: symbol
        for expression in identities.values()
        for symbol in expression.free_symbols
    }
    compactness = symbol_map["C"]
    ratio = symbol_map["r"]
    radial_1 = symbol_map["A1"]
    angular_1 = symbol_map["B1"]
    expected_f = (
        (3 * ratio**2 + 6 * ratio + 1) * radial_1
        + 4 * angular_1
        + compactness * (6 * ratio**2 + 18 * ratio + 8)
    ) / (18 * compactness * (1 + ratio))
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-713"
    ]
    variables = {
        row.get("symbol"): row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol")
        in {
            "s_compact_MTS",
            "sigma_prime_compact_MTS",
            "kappa4_compact_MTS",
            "D4_ADM_completion_MTS",
            "q3_l1_parent_MTS",
        }
    }
    checkpoint = (
        POST
        / "4871-Y5-R2FR-v3-l1-asymptotic-kappa4-crosscheck-and-full-first-order-C3-arbitration.md"
    ).read_text(encoding="utf-8")
    formal = (
        FORMAL / "887-PPC4161-v3-tail-kappa4-and-C3-arbitration.md"
    ).read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4870_VALIDATION.csv")
    arb = arbitration()
    maximum_kappa_gap = max(
        float(row["kappa4_absolute_difference"]) for row in grid
    )
    maximum_first_variation = max(
        abs(float(row["l2_first_variation_extrapolated"])) for row in grid
    )

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    groups = (
        sources,
        equations,
        surfaces,
        source_c3,
        parity,
        decomposition,
        arbitration_data,
        decisions,
        residuals,
    )
    checks = [
        result("VAL4871_00_sources", len(sources) == 23 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        result("VAL4871_01_equation", len(equations) == 7 and equations[2]["derived"] == "H2[q1]*q3=-E4[q1]", "third-order equation and boundaries recorded"),
        result("VAL4871_02_surface", len(surfaces) == 4 and all(row["status"] == "DERIVED_EXACT" for row in surfaces), "four exact surface identities generated"),
        result("VAL4871_03_first_map", sp.simplify(identities["f_surface"] - expected_f) == 0, "surface v coefficient reproduces first-response Ward map"),
        result("VAL4871_04_grid", len(grid) == 5 and all(row["status"] == "PASS" for row in grid), "five finite-C tail rows pass"),
        result("VAL4871_05_kappa_gap", maximum_kappa_gap < 1.83e-8, f"maximum gap={maximum_kappa_gap:.9g}"),
        result("VAL4871_06_stationarity", maximum_first_variation < 5.7e-8, f"maximum extrapolated variation={maximum_first_variation:.9g}"),
        result("VAL4871_07_C3_sources", len(source_c3) == 2 and all(row["formula_matches_v2"] and row["missing_binary_operator_before_last_term"] for row in source_c3), "v1/v2 formula identity and missing operator audited"),
        result("VAL4871_08_parity", len(parity) == 3 and all(4.95 < float(row["a3_odd_estimator"]) < 4.97 for row in parity), "three refined parent parity rows controlled"),
        result("VAL4871_09_a2", abs(arb["parent_a2_intercept"] - arb["published_a2"]) < 3.0e-7, "published quadratic coefficient reproduced"),
        result("VAL4871_10_a3", 4.95 < arb["parent_a3_intercept"] < 4.97, f"parent a3={arb['parent_a3_intercept']:.10g}"),
        result("VAL4871_11_external", arb["minimum_plus_gap"] > 5.86 and not arb["single_omit_or_sign_flip_resolves"], "external variants remain disjoint"),
        result("VAL4871_12_ambiguity", arb["ambiguous_final_alpha1_squared_alpha2_term_vanishes"], "printed ambiguous term vanishes on r=1/3 slice"),
        result("VAL4871_13_decision", decisions[4]["decision"] == "SELECT_INTERNAL" and decisions[5]["decision"] == "DEMOTE_EXTERNAL_SOURCE_DISCREPANCY", "parent branch selected without claiming erratum"),
        result("VAL4871_14_residual", residuals[0]["status"] == "CLOSED_PARENT" and residuals[8]["status"] == "OPEN_HARD_NEXT", "compact tail closed and primitive action selected next"),
        result("VAL4871_15_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group) and all(row.get("valid_for_claim") == "False" for row in grid), "all rows private nonclaim"),
        result("VAL4871_16_registers", len(claims) == 1 and claims[0].get("status") == "v3_surface_kappa4_crosscheck_closed_parent_C3_selected_internal_external_printed_C3_demoted_source_discrepancy_private_nonclaim" and variables.get("q3_l1_parent_MTS", {}).get("status") == "derived_finite_C_parent_profile_asymptotic_kappa4_crosscheck_nonclaim" and variables.get("kappa4_compact_MTS", {}).get("status") == "finite_C_parent_response_derived_v3_surface_crosschecked_binary_safe_primitive_ownership_open_nonclaim" and variables.get("D4_ADM_completion_MTS", {}).get("status") == "derived_charge_partition_v3_surface_crosschecked_not_independent_parent_response_nonclaim", "claim and compact-response variables integrated"),
        result("VAL4871_17_documents", "V3_L1_SURFACE_KAPPA4_AND_C3_ARBITRATION_4871" in checkpoint and "PPC4161_V3_TAIL_KAPPA4_C3_ARBITRATION_4871" in formal, "checkpoint and formal markers found"),
        result("VAL4871_18_resume", resume_checkpoint_at_least(resume, 4871) and NEXT_TARGET in resume, "resume returns to primitive action ownership"),
        result("VAL4871_19_prior", prior[-1].get("status") == "PASS", "4870 validation remains historical green"),
        result("VAL4871_20_scripts", all(compiles(path) for path in (Path(__file__).resolve(), POST / "scripts" / "Y5_R2FR_4871_v3_asymptotic_response.py", POST / "scripts" / "Y5_R2FR_4871_asymptotic_surface_identity.py", POST / "scripts" / "Y5_R2FR_4871_v3_grid_runner.py", POST / "scripts" / "Y5_R2FR_4871_C3_source_arbitration.py")), "all 4871 scripts compile"),
        result("VAL4871_21_pycache", not (POST / "scripts" / "__pycache__").exists(), "no scripts pycache directory"),
    ]
    checks.append(
        result(
            "VAL4871_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "V3_L1_SURFACE_KAPPA4_AND_C3_ARBITRATION_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    equations = v3_equation_rows()
    surfaces = surface_rows()
    grid = read_csv(GRID_PATH)
    source_c3 = with_metadata(source_audit())
    parity = with_metadata(parent_parity_rows())
    decomposition = with_metadata(external_decomposition())
    arbitration_data = arbitration_rows()
    decisions = decision_rows()
    residuals = residual_rows()
    validation = validation_rows(
        sources,
        equations,
        surfaces,
        grid,
        source_c3,
        parity,
        decomposition,
        arbitration_data,
        decisions,
        residuals,
    )
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_V3_EQUATION.csv", equations)
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_ASYMPTOTIC_SURFACE_IDENTITY.csv", surfaces)
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_C3_SOURCE_AUDIT.csv", source_c3)
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_C3_PARENT_PARITY.csv", parity)
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_C3_EXTERNAL_DECOMPOSITION.csv", decomposition)
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_C3_ARBITRATION.csv", arbitration_data)
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4871_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4871_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4871_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4871_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
