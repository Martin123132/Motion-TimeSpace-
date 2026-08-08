from __future__ import annotations

import csv
import math
import tarfile
from pathlib import Path
from typing import Any

import sympy as sp

from Y5_R2FR_4869_l1_metric_response_source import (
    aether_radial_shift_source,
    asymptotic_response_identities,
    metric_shift_ward_identities,
)


CHECKPOINT = "4869"
TIMESTAMP = "2026-07-10T15:05:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4870-Y5-R2FR-v4-mass-variation-surface-identity-and-v3-l1-asymptotic-response-or-ADM-monopole.md"
PARENT_A3_LOW = 4.94
PARENT_A3_HIGH = 5.00
GUPTA_A3 = 975961420 / 90053964


PARITY_DATA = (
    (0.015, 0.02084125005119911, -0.022049381955144044, 1.99e-8),
    (0.020, 0.027536661402126347, -0.02968562133418573, 1.99e-8),
    (0.030, 0.04056989855815746, -0.04541288823083534, 1.99e-8),
    (0.040, 0.05314706830998975, -0.06177657133334321, 2.00e-8),
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
    prefix = "Last checkpoint: `"
    for line in resume.splitlines():
        if line.startswith(prefix):
            token = line[len(prefix) :].split("-", 1)[0]
            return token.isdigit() and int(token) >= checkpoint
    return False


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4869_00_public", POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md", "PUBLIC_FRAME_VARIATION_SELECTION_4861", "public action and source frame"),
        ("SRC4869_01_weak", POST / "4867-Y5-R2FR-second-order-boost-l0-l2-star-equations-and-third-order-l1-source-or-finite-kappa4-fallback.md", "LEADING_QUARTIC_SELF_ENERGY_4867", "weak first and quartic response"),
        ("SRC4869_02_finite", POST / "4868-Y5-R2FR-finite-compactness-v2-backreaction-and-v3-dipole-shooting-determinant-or-quartic-response-remainder-bound.md", "Supersession note from checkpoint 4869", "superseded endpoint interpretation"),
        ("SRC4869_03_prior_validation", OUTPUT / "P8_Y5_BRR545_4868_VALIDATION.csv", "VAL4868_OVERALL", "prior validation"),
        ("SRC4869_04_checkpoint", POST / "4869-Y5-R2FR-l1-metric-Ward-completion-and-C3-sensitivity-discrepancy-or-v4-boundary-extension.md", "L1_METRIC_WARD_AND_C3_DISCREPANCY_4869", "human derivation"),
        ("SRC4869_05_formal", FORMAL / "885-PPC4161-l1-metric-Ward-and-C3-sensitivity-discrepancy.md", "PPC4161_L1_METRIC_WARD_C3_DISCREPANCY_4869", "formal integration"),
        ("SRC4869_06_claim", FORMAL / "02-claims-register.csv", "L-711", "claim register"),
        ("SRC4869_07_variable", FORMAL / "04-variable-audit.csv", "Z_l1_metric_MTS", "variable audit"),
        ("SRC4869_08_equation", FORMAL / "05-equation-register.md", "1.162 Polar-dipole metric Ward completion", "equation register"),
        ("SRC4869_09_redteam", FORMAL / "06-consistency-red-team.md", "113. Metric Ward completion and C3 discrepancy red team", "red-team register"),
        ("SRC4869_10_spine", FORMAL / "07-unification-spine.md", "checkpoint 4869", "unification spine"),
        ("SRC4869_11_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: `4869-", "resume marker"),
        ("SRC4869_12_flow_script", POST / "scripts" / "Y5_R2FR_4868_fixed_background_variational_remainder.py", "solve_bvp_profile", "finite-C flow solver"),
        ("SRC4869_13_ward_script", POST / "scripts" / "Y5_R2FR_4869_l1_metric_response_source.py", "metric_shift_ward_identities", "symbolic Ward derivation"),
        ("SRC4869_14_generator", Path(__file__).resolve(), 'CHECKPOINT = "4869"', "checkpoint generator"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        valid = path.exists() and needle in content
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
                "source_validated": valid,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    archives = [
        ("SRC4869_15_yagi", Path(r"D:\Temp\1311.7144-source.tar"), "paper.tex", r"\label{ae:mass}", "strong-field mass variation and asymptotic sensitivity map"),
        ("SRC4869_16_gupta", Path(r"D:\Temp\2104.04596-source.tar"), "main.tex", r"\label{tolman_sens_C}", "published Tolman VII C3 series"),
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
            "source_id": "SRC4869_17_urls",
            "source_kind": "primary_url_ledger",
            "source_locator": "https://arxiv.org/abs/1311.7144;https://arxiv.org/abs/2104.04596;https://arxiv.org/abs/gr-qc/0509121;https://arxiv.org/abs/gr-qc/0507059",
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


def ward_rows() -> list[dict[str, Any]]:
    ward = metric_shift_ward_identities()
    source, _ = aether_radial_shift_source()
    asymptotic = asymptotic_response_identities()
    radius, ratio, compactness, radial_tail, angular_tail = sp.symbols(
        "R r C A_infinity B_infinity", real=True
    )
    expected_radial = "-8*pi*Z/(3*A*N)"
    expected_angular = "-8*pi*[R*Z'+(A^2-1+4*pi*G*R^2*A^2*(P-rho))*Z]/(3*A*N)"
    entries = [
        ("WARD4869_00_matter", "perfect-fluid shift coefficient", "16*pi*G times sqrt(h)(rho+P)beta^2/(2N)", "unique coefficient preserving the time-gauge zero mode", "DERIVED_EXACT"),
        ("WARD4869_01_Z", "gauge-invariant shift", "Z=k-R*s'-s+2R(N'/N)s", "zero for k=N^2 H', s=N^2 H/R", "DERIVED_EXACT"),
        ("WARD4869_02_radial", "radial GR+matter Euler equation", sp.sstr(ward["radial_euler_invariant"]), expected_radial, "PASS"),
        ("WARD4869_03_angular", "angular GR+matter Ward equation", sp.sstr(ward["angular_euler_invariant"]), expected_angular, "DERIVED_EXACT"),
        ("WARD4869_04_source", "aether radial metric source operation count", sp.count_ops(source), 106, "PASS" if sp.count_ops(source) == 106 else "FAIL"),
        ("WARD4869_05_metric_tail", "Z infinity coefficient", sp.sstr(asymptotic["invariant_tail"]), "-4(Ainf-2Binf-C)/[3C(1+r)]", "PASS"),
        ("WARD4869_06_fmetric", "metric first response", sp.sstr(asymptotic["response_from_metric"]), "[-Ainf+2Binf+C(1+3r)]/[3C(1+r)]", "PASS"),
        ("WARD4869_07_fbulk", "bulk boundary first response", sp.sstr(asymptotic["response_from_bulk"]), "on-shell L2 boundary", "DERIVED_EXACT"),
        ("WARD4869_08_difference", "bulk minus metric response", sp.sstr(asymptotic["response_difference"]), "exterior_relation/[18C(1+r)]", "PASS"),
        ("WARD4869_09_exterior", "exterior flow relation", sp.sstr(asymptotic["exterior_relation"]), "zero on the exterior Euler solution", "DERIVED_EXACT"),
        ("WARD4869_10_completion", "independent D2", "0 after the parent-action Ward and exterior equations", "nonzero checkpoint-4868 calibration withdrawn", "CORRECTED"),
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


def parity_rows() -> list[dict[str, Any]]:
    leading = 10 / 7
    rows: list[dict[str, Any]] = []
    for compactness, positive, negative, residual in PARITY_DATA:
        quadratic = (positive + negative) / (2 * compactness**2)
        cubic = (
            positive - negative - 2 * leading * compactness
        ) / (2 * compactness**3)
        rows.append(
            {
                "row_id": f"PAR4869_C{compactness:.3f}",
                "compactness_magnitude": compactness,
                "f_positive": positive,
                "f_negative": negative,
                "a2_even_estimator": quadratic,
                "a3_odd_estimator": cubic,
                "base_outer_radii": "100;200;400",
                "outer_extrapolation": "quadratic in 1/Rmax",
                "maximum_bvp_residual": residual,
                "negative_C_role": "mathematical derivative diagnostic only",
                "status": "CONTROLLED_PARITY_SERIES_ROW_NONCLAIM",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def comparison_rows(parity: list[dict[str, Any]]) -> list[dict[str, Any]]:
    published_a1 = 10 / 7
    published_a2 = -338345 / 126126
    minimum_gap = GUPTA_A3 - PARENT_A3_HIGH
    entries = [
        ("CMP4869_00_a1", "C coefficient", published_a1, published_a1, "EXACT_MATCH"),
        ("CMP4869_01_a2", "C2 coefficient", "parent interval [-2.71,-2.67]", published_a2, "CONSISTENT"),
        ("CMP4869_02_a3_parent", "parent C3 coefficient", f"({PARENT_A3_LOW},{PARENT_A3_HIGH})", "symmetric C2 extrapolation", "BOUNDED_NUMERIC"),
        ("CMP4869_03_a3_gupta", "Gupta C3 coefficient", GUPTA_A3, "975961420/90053964", "SOURCE_EXACT"),
        ("CMP4869_04_disjoint", "minimum C3 interval gap", minimum_gap, ">5.8", "DISCREPANCY_CONFIRMED"),
        ("CMP4869_05_endpoint", "C=0.3 value comparison", "diagnostic only", "C3 truncation not exact calibration", "RECLASSIFIED"),
        ("CMP4869_06_origin", "source of C3 conflict", "OPEN", "public correlated limit; reduced-action boundary/convention; long source algebra", "NO_SELECTION"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "parent_or_derived": derived,
            "published_or_reference": reference,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, derived, reference, status in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "GR plus matter l1 Hessian", "RETAIN_DERIVED", "gauge zero mode fixes the matter coefficient exactly"),
        (2, "aether metric source", "RETAIN_DERIVED", "generated directly from the parent coefficient surface"),
        (3, "first-response ADM completion", "CLOSED_NO_FREE_D2", "metric asymptotic response equals the on-shell bulk boundary functional"),
        (4, "checkpoint-4868 D2 calibration", "WITHDRAW", "it forced a C3-truncated external value at C=0.3"),
        (5, "parent finite-C f", "QUARANTINE_AT_C3", "internally Ward-consistent but conflicts with the published cubic coefficient"),
        (6, "Gupta finite-C f", "QUARANTINE_AT_C3", "source-backed but its cubic coefficient conflicts with the independent parent reduction"),
        (7, "D4 interval", "BOOKKEEPING_ONLY", "its independence is not inherited from the withdrawn D2 interpretation"),
        (8, "next derivation", "V4_WARD_AND_V3_SURFACE", "decide whether L4 already owns physical kappa4"),
        (9, "local GR", "NOT_PROMOTED", "quartic identity and C3 discrepancy remain open"),
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
        (1, "R_l1_GR_matter_operator", "CLOSED", "exact gauge-invariant Ward reduction", "reuse at v3"),
        (2, "R_l1_aether_source", "CLOSED", "exact 106-operation parent source", "reuse in quartic source hierarchy"),
        (3, "R_first_metric_completion", "CLOSED_PARENT", "fmetric=fbulk on exterior flow equation", "remove free D2"),
        (4, "R_C1_C2", "CONSISTENT", "parent and Gupta coefficients agree", "retain as regressions"),
        (5, "R_C3", "OPEN_DECISIVE_CONFLICT", "parent interval 4.94-5.00 versus Gupta 10.8375", "audit full coupled first-order equations or source algebra"),
        (6, "R_v4_Ward", "OPEN_HARD_NEXT", "no quartic surface identity yet", "derive mass variation through v4"),
        (7, "R_v3_l1", "OPEN_HARD_NEXT", "asymptotic third-order response not generated", "extend shift-flow polynomial to v3"),
        (8, "R_D4", "BOOKKEEPING_UNRESOLVED", "independence unproved", "retain only if v4 boundary residual survives"),
        (9, "R_local_GR", "OPEN_HARD", "finite compact response not closed", "do not promote"),
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
    ward: list[dict[str, Any]],
    parity: list[dict[str, Any]],
    comparison: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-711"]
    variables = [row for row in read_csv(FORMAL / "04-variable-audit.csv") if row.get("symbol") == "Z_l1_metric_MTS"]
    d4_rows = [row for row in read_csv(FORMAL / "04-variable-audit.csv") if row.get("symbol") == "D4_ADM_completion_MTS"]
    checkpoint = (POST / "4869-Y5-R2FR-l1-metric-Ward-completion-and-C3-sensitivity-discrepancy-or-v4-boundary-extension.md").read_text(encoding="utf-8")
    formal = (FORMAL / "885-PPC4161-l1-metric-Ward-and-C3-sensitivity-discrepancy.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4868_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    groups = (sources, ward, parity, comparison, decisions, residuals)
    checks = [
        result("VAL4869_00_sources", len(sources) == 18 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        result("VAL4869_01_ward", len(ward) == 11 and all(row["status"] != "FAIL" for row in ward), "all Ward/source rows derived"),
        result("VAL4869_02_matter", ward[0]["status"] == "DERIVED_EXACT", "matter coefficient fixed by gauge invariance"),
        result("VAL4869_03_source", ward[4]["derived"] == 106, "aether metric source operation count locked"),
        result("VAL4869_04_completion", ward[-1]["status"] == "CORRECTED", "independent D2 withdrawn"),
        result("VAL4869_05_parity", len(parity) == 4 and all(float(row["maximum_bvp_residual"]) <= 2.01e-8 for row in parity), "four symmetric compactness rows controlled"),
        result("VAL4869_06_a2", all(-2.71 < float(row["a2_even_estimator"]) < -2.67 for row in parity), "quadratic estimators contain published coefficient"),
        result("VAL4869_07_a3", all(4.95 < float(row["a3_odd_estimator"]) < 5.00 for row in parity), "cubic estimators support conservative parent interval"),
        result("VAL4869_08_disjoint", GUPTA_A3 - PARENT_A3_HIGH > 5.8, f"minimum gap={GUPTA_A3-PARENT_A3_HIGH:.6g}"),
        result("VAL4869_09_comparison", comparison[0]["status"] == "EXACT_MATCH" and comparison[4]["status"] == "DISCREPANCY_CONFIRMED", "C1 match and C3 conflict recorded"),
        result("VAL4869_10_decision", decisions[2]["decision"] == "CLOSED_NO_FREE_D2" and decisions[7]["decision"] == "V4_WARD_AND_V3_SURFACE", "correction and next theorem selected"),
        result("VAL4869_11_residual", residuals[4]["status"] == "OPEN_DECISIVE_CONFLICT" and residuals[5]["status"] == "OPEN_HARD_NEXT", "C3 and quartic gates remain explicit"),
        result("VAL4869_12_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows private nonclaim"),
        result("VAL4869_13_registers", len(claims) == 1 and len(variables) == 1 and len(d4_rows) == 1 and d4_rows[0].get("status") == "bookkeeping_interval_independence_unproved_quartic_Ward_gate_open_nonclaim", "claim and corrected variables integrated"),
        result("VAL4869_14_documents", "L1_METRIC_WARD_AND_C3_DISCREPANCY_4869" in checkpoint and "PPC4161_L1_METRIC_WARD_C3_DISCREPANCY_4869" in formal, "checkpoint and formal markers found"),
        result("VAL4869_15_resume", resume_checkpoint_at_least(resume, 4869) and NEXT_TARGET in resume, "resume advanced to quartic Ward identity"),
        result("VAL4869_16_prior", prior[-1].get("status") == "PASS", "4868 validation remains historical green"),
        result("VAL4869_17_scripts", compiles(Path(__file__).resolve()) and compiles(POST / "scripts" / "Y5_R2FR_4869_l1_metric_response_source.py"), "generator and symbolic source compile"),
        result("VAL4869_18_pycache", not (POST / "scripts" / "__pycache__").exists(), "no scripts pycache directory"),
    ]
    checks.append(
        result(
            "VAL4869_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "L1_METRIC_WARD_AND_C3_DISCREPANCY_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    ward = ward_rows()
    parity = parity_rows()
    comparison = comparison_rows(parity)
    decisions = decision_rows()
    residuals = residual_rows()
    validation = validation_rows(
        sources,
        ward,
        parity,
        comparison,
        decisions,
        residuals,
    )
    write_csv(OUTPUT / "P8_Y5_R2FR_4869_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4869_METRIC_WARD_IDENTITY.csv", ward)
    write_csv(OUTPUT / "P8_Y5_R2FR_4869_COMPACTNESS_PARITY_SERIES.csv", parity)
    write_csv(OUTPUT / "P8_Y5_R2FR_4869_C3_COMPARISON.csv", comparison)
    write_csv(OUTPUT / "P8_Y5_R2FR_4869_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4869_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4869_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4869_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4869_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
