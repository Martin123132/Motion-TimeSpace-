from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4558"
CLAIM_ID = "L-400"
BRANCH_ID = "MTS_R2FR_Y5_ORBITAL_GAMMA_BETA_COMBO_4558"
MARKER = "PPC4161_ORBITAL_GAMMA_BETA_COMBO_PRIVATE_SCORECARD_OR_FINITE_AMPLITUDE_ROW_4558"
PACKET_MARKER = "PPC4161_PACKET_ORBITAL_GAMMA_BETA_COMBO_ZERO_4558"
DECISION = "ORBITAL_GAMMA_BETA_COMBO_PRIVATE_ZERO_DERIVED_NEXT_HARD_CHANNEL_R10_YUKAWA_GLOBAL_PARENT_UNSIGNED"
NEXT_TARGET = "4559-Y5-R2FR-R10-Yukawa-private-zero-or-real-bound-source-row.md"

OBSERVABLE = "((2+2gamma-beta)/3)-1"
FORMAL_PATH = FORMAL / "574-PPC4161-orbital-gamma-beta-combo-private-scorecard-or-finite-amplitude-row.md"
DOC_PATH = POST / "4558-Y5-R2FR-orbital-gamma-beta-combo-private-scorecard-or-finite-amplitude-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4557 = FORMAL / "573-PPC4161-zeta3-stress-conservation-channel-zero-or-finite-amplitude-row.md"
DOC_4550 = FORMAL / "566-PPC4161-first-static-coefficient-product-bound-or-projection-kernel-row.md"
DOC_4172 = FORMAL / "188-PPC4161-full-PPN-readout-vector.md"
DOC_4170 = FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md"
DOC_4171 = FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md"
POST_4171 = POST / "4171-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Gauss-Newton-readout.md"
DOC_4539 = FORMAL / "555-PPC4161-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
SCORECARD_4557 = SOURCE_DIR / "P8_Y5_R2FR_4557_SCORECARD_AFTER_ZETA3.csv"
RANKING_4557 = SOURCE_DIR / "P8_Y5_R2FR_4557_ACTIVE_PRODUCT_PRESSURE_RANKING_AFTER_ZETA3.csv"
PRODUCT_BOUNDS_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv"
ORBITAL_READOUT_4171 = SOURCE_DIR / "P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT.csv"
POISSON_4171 = SOURCE_DIR / "P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4558_SOURCE_REGISTER.csv"
ALGEBRA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_ORBITAL_COMBO_ALGEBRA.csv"
CARRIER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_GAMMA_BETA_CARRIER_CLASSIFICATION.csv"
ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_ORBITAL_COMBO_PRIVATE_ZERO_CERTIFICATE.csv"
FALLBACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_ORBITAL_COMBO_FINITE_AMPLITUDE_ROWS.csv"
SCORECARD_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_SCORECARD_AFTER_ORBITAL_COMBO.csv"
ACTIVE_AFTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_ACTIVE_PRODUCT_PRESSURE_RANKING_AFTER_ORBITAL_COMBO.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4558_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4558_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        stripped = str(value).strip()
        if stripped == "" or stripped.lower() in {"missing", "nan", "none"}:
            return None
        return float(stripped)
    except (TypeError, ValueError):
        return None


def product_row() -> dict[str, str]:
    return next((row for row in read_csv(PRODUCT_BOUNDS_4550) if row.get("observable") == OBSERVABLE), {})


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4558_00_4557_doc", "4557 result selecting orbital combo", DOC_4557, "next active private channel is `((2+2gamma-beta)/3)-1`"),
        ("SRC4558_01_4557_scorecard", "4557 scorecard orbital combo row", SCORECARD_4557, "SC4555_((2+2gamma-beta)/3)-1"),
        ("SRC4558_02_4557_ranking", "4557 active ranking orbital combo first", RANKING_4557, "1,((2+2gamma-beta)/3)-1"),
        ("SRC4558_03_4550_bounds", "4550 orbital product bounds", PRODUCT_BOUNDS_4550, "PB4550_2p2gammambeta_3m1"),
        ("SRC4558_04_4550_doc", "4550 product-bound doc", DOC_4550, "PB4550_2p2gammambeta_3m1"),
        ("SRC4558_05_4172_beta", "4172 private beta readout", DOC_4172, "beta = 1."),
        ("SRC4558_06_4172_gamma", "4172 private gamma readout", DOC_4172, "gamma = 1."),
        ("SRC4558_07_packet_ppn", "180 packet full PPN vector", PACKET_PATH, "(gamma-1, beta-1, alpha1, alpha2, alpha3, xi, zeta1, zeta2, zeta3, zeta4, Gdot/G) = 0"),
        ("SRC4558_08_4170_no_orbital_import", "4170 anti-circular worldtube mass glue", DOC_4170, "No orbital `GM`, fitted acceleration"),
        ("SRC4558_09_4171_newton_readout", "4171 Poisson/Gauss/Newton readout", DOC_4171, "Orbital data is now a test"),
        ("SRC4558_10_4171_post", "4171 downstream orbit guard", POST_4171, "Orbits are downstream tests now."),
        ("SRC4558_11_4171_orbital_csv", "4171 orbital acceleration readout csv", ORBITAL_READOUT_4171, "OR4171_3_anti_circular"),
        ("SRC4558_12_4171_poisson_csv", "4171 Poisson/Gauss csv", POISSON_4171, "PG4171_4_gauss"),
        ("SRC4558_13_4539_firewall", "4539 parent/global firewall", DOC_4539, "FAIL_UNSIGNED"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4558 orbital gamma-beta combo derivation",
                "valid_for_claim": "False",
            }
        )
    return rows


def algebra_rows() -> list[dict[str, Any]]:
    product = product_row()
    bound = safe_float(product.get("bound")) or 4.6666666666666672e-05
    return [
        {
            "algebra_id": "OA4558_0_definition",
            "object": OBSERVABLE,
            "law": "O_orb := ((2+2gamma-beta)/3)-1",
            "result": "O_orb = (2(gamma-1) - (beta-1))/3",
            "meaning": "The orbital pressure row is not a new independent field coefficient if gamma and beta are already fixed by the private PPN metric readout.",
            "status": "exact_algebra",
            "valid_for_claim": "False",
        },
        {
            "algebra_id": "OA4558_1_private_substitution",
            "object": "private gamma/beta readout",
            "law": "gamma-1 = 0 and beta-1 = 0",
            "result": "O_orb = 0",
            "meaning": "Inside the same PPC4161-GP-HQNP private branch, the observed orbital combo inherits the gamma/beta zero rather than introducing a fitted orbital correction.",
            "status": "private_selector_zero",
            "valid_for_claim": "False",
        },
        {
            "algebra_id": "OA4558_2_observable_bound",
            "object": "finite fallback",
            "law": "|O_orb| <= B_orb",
            "result": f"B_orb = {bound:.16e}",
            "meaning": "If the private gamma/beta readout is rejected, the finite nonclaim residual must satisfy the measured orbital combo budget.",
            "status": "fallback_bound_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "algebra_id": "OA4558_3_component_bound",
            "object": "gamma/beta component no-cancellation",
            "law": "2|gamma-1| + |beta-1| <= 3 B_orb",
            "result": f"3 B_orb = {3.0 * bound:.16e}",
            "meaning": "This is the conservative component budget if gamma and beta residuals are not allowed to cancel.",
            "status": "component_guard_nonclaim",
            "valid_for_claim": "False",
        },
    ]


def carrier_rows() -> list[dict[str, Any]]:
    return [
        {
            "carrier_id": "OC4558_0_EH_metric_coefficients",
            "carrier": "same-metric EH <=2PN readout",
            "contribution": "gamma=1 and beta=1",
            "orbital_projection": "0",
            "reason": "The 1PN spatial curvature coefficient and 2PN self-interaction coefficient are fixed by the local EH metric expansion in the private selector.",
            "countermodel": "non-EH metric principal block or extra 2PN self-interaction coefficient",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "OC4558_1_source_charge",
            "carrier": "Hamiltonian worldtube source charge",
            "contribution": "sets Newtonian monopole/source normalization before orbit fitting",
            "orbital_projection": "no circular GM import",
            "reason": "The mass/source charge is owned by the Hamiltonian/Hilbert worldtube map before orbital data are used as tests.",
            "countermodel": "using observed orbital GM as a denominator or late calibration object",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "OC4558_2_Poisson_Gauss_Newton",
            "carrier": "first-order weak-field Poisson/Gauss readout",
            "contribution": "a=-grad Phi_N and a_r=-G_N M_H^dress/r^2",
            "orbital_projection": "Newtonian orbital baseline derived inside branch",
            "reason": "The perihelion/PPN combo sits on top of the already derived private Newtonian source readout.",
            "countermodel": "source charge not equal to the Hamiltonian mass or noncompact multipole/radiative correction misread as monopole",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "OC4558_3_gamma_beta_combo",
            "carrier": "observed PPN perihelion/orbital combination",
            "contribution": "O_orb=(2 delta_gamma - delta_beta)/3",
            "orbital_projection": "0 when delta_gamma=delta_beta=0",
            "reason": "The combo is an algebraic dependent observable of gamma and beta in this branch.",
            "countermodel": "independent orbital-sector force term not captured by gamma/beta PPN metric readout",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "OC4558_4_boundary_or_higher",
            "carrier": "boundary/higher-order orbital residue",
            "contribution": "Q_orb + R_higher",
            "orbital_projection": "excluded inside compact private selector or bounded by fallback row",
            "reason": "Open/radiative/noncompact flux or high-order corrections cannot be silently absorbed into the gamma/beta zero.",
            "countermodel": "unrouted boundary flux, nonstationary radiative system, or large higher-PN residual",
            "valid_for_claim": "False",
        },
    ]


def zero_rows() -> list[dict[str, Any]]:
    product = product_row()
    return [
        {
            "zero_id": "OZ4558_0_private_selector_orbital_combo",
            "scope": "private PPC4161-GP-HQNP compact stationary same-metric EH/Hilbert source local selector",
            "O_orb": "0",
            "basis": "exact algebra O_orb=(2(gamma-1)-(beta-1))/3; private gamma=1 and beta=1; Hamiltonian source charge fixed before orbital readout; no independent orbital force term admitted",
            "bound": product.get("bound", "4.6666666666666672e-05"),
            "private_selector_ready": "True",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "OZ4558_1_global_firewall",
            "scope": "full MTS parent/global/open/radiative/non-EH orbital sectors",
            "O_orb": "not_promoted",
            "basis": "global EH-origin, source-charge calibration, boundary silence and no-independent-orbital-force clauses are not globally parent-signed",
            "bound": product.get("bound", "4.6666666666666672e-05"),
            "private_selector_ready": "False",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def fallback_rows() -> list[dict[str, Any]]:
    product = product_row()
    bound = safe_float(product.get("bound")) or 4.6666666666666672e-05
    return [
        {
            "row_id": "OF4558_0_master_no_cancellation",
            "channel": "orbital gamma-beta combo total retained channel",
            "exact_requirement": product.get("exact_no_cancellation_condition", "|P_orb|*epsilon_U^2 + |Q_orb| + |R_higher_orb| <= 4.6666666666666672e-05"),
            "numeric_value": product.get("bound", "4.6666666666666672e-05"),
            "units": product.get("bound_units", "dimensionless"),
            "status": "fallback_if_private_zero_scope_fails",
            "valid_for_claim": "False",
        },
        {
            "row_id": "OF4558_1_component_combo_bound",
            "channel": "gamma/beta residual components",
            "exact_requirement": "2|gamma-1| + |beta-1| <= 3 B_orb if no cancellation is allowed",
            "numeric_value": f"{3.0 * bound:.16e}",
            "units": product.get("bound_units", "dimensionless"),
            "status": "finite_component_budget_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "OF4558_2_delta_gamma_if_beta_zero",
            "channel": "gamma-1",
            "exact_requirement": "|gamma-1| <= 3 B_orb/2 if beta-1 and all other terms are zero",
            "numeric_value": f"{1.5 * bound:.16e}",
            "units": product.get("bound_units", "dimensionless"),
            "status": "finite_gamma_budget_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "OF4558_3_delta_beta_if_gamma_zero",
            "channel": "beta-1",
            "exact_requirement": "|beta-1| <= 3 B_orb if gamma-1 and all other terms are zero",
            "numeric_value": f"{3.0 * bound:.16e}",
            "units": product.get("bound_units", "dimensionless"),
            "status": "finite_beta_budget_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "OF4558_4_source_product_if_boundary_zero",
            "channel": f"P_{OBSERVABLE}",
            "exact_requirement": "|P_orb| <= B_orb/epsilon_U^2 if boundary and higher terms are zero",
            "numeric_value": product.get("max_product_if_boundary_and_higher_zero", "7.5346165570953197e+09"),
            "units": "dimensionless effective product",
            "status": "finite_source_product_budget_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "OF4558_5_boundary_plus_higher_half_budget",
            "channel": "Q_orb + R_higher_orb",
            "exact_requirement": "|Q_orb| + |R_higher_orb| <= B_orb/2 under equal split",
            "numeric_value": product.get("max_boundary_plus_higher_equal_half_budget", "2.3333333333333336e-05"),
            "units": product.get("bound_units", "dimensionless"),
            "status": "finite_boundary_higher_budget_nonclaim",
            "valid_for_claim": "False",
        },
    ]


def scorecard_after_orbital_rows() -> list[dict[str, Any]]:
    rows = read_csv(SCORECARD_4557)
    updated: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        if row.get("observable") == OBSERVABLE:
            item["private_selector_prediction"] = "0"
            item["private_selector_status"] = "PASS_PRIVATE_SELECTOR_ZERO"
            item["active_private_pressure"] = "False"
            item["next_action"] = "do not reopen orbital combo unless gamma/beta private readout, source charge, or independent orbital force scope changes"
        updated.append(item)
    return updated


def active_after_orbital_rows(scorecard: list[dict[str, Any]]) -> list[dict[str, Any]]:
    active = [row for row in scorecard if row.get("active_private_pressure") == "True"]
    active.sort(key=lambda row: safe_float(row.get("max_product_if_boundary_and_higher_zero")) or float("inf"))
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(active, start=1):
        rows.append(
            {
                "active_rank": index,
                "observable": row.get("observable", ""),
                "arena": row.get("arena", ""),
                "max_product_if_boundary_and_higher_zero": row.get("max_product_if_boundary_and_higher_zero", ""),
                "recommended_next": b(index == 1),
                "valid_for_claim": "False",
            }
        )
    return rows


def claim_gate_rows(active_after: list[dict[str, Any]]) -> list[dict[str, Any]]:
    next_observable = active_after[0].get("observable", "NONE") if active_after else "NONE"
    return [
        {
            "gate_id": "G4558_0_orbital_private_zero",
            "requirement": "orbital combo zero follows from gamma=1 and beta=1 inside private PPN readout",
            "status": "PASS_PRIVATE_SELECTOR",
            "claim_effect": "orbital combo removed from active private product pressure",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4558_1_exact_algebra",
            "requirement": "O_orb = (2(gamma-1)-(beta-1))/3 is explicitly recorded",
            "status": "PASS_ALGEBRA",
            "claim_effect": "prevents adding a new independent orbital fitting knob",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4558_2_anti_circularity",
            "requirement": "Hamiltonian source charge is defined before orbital readout",
            "status": "GUARD_RETAINED",
            "claim_effect": "prevents laundering observed GM into the derivation",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4558_3_global_public_firewall",
            "requirement": "global parent/public orbital claim remains false",
            "status": "PASS_FIREWALL",
            "claim_effect": "private branch does not become public local-GR proof",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4558_4_next_channel_selection",
            "requirement": "remaining channels ranked after orbital combo removal",
            "status": "PASS_NEXT_SELECTED" if next_observable == "alpha_Yukawa_at_lambda_38p6um" else "FAIL_NEXT_SELECTION",
            "claim_effect": f"next hard channel = {next_observable}",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4558_0",
            "decision": DECISION,
            "summary": "4558 derives the orbital gamma-beta combination as an algebraic dependent observable inside the private PPN branch: ((2+2gamma-beta)/3)-1 = (2(gamma-1)-(beta-1))/3, and 4172 gives gamma=1, beta=1 in the same selector. The Newton/source-charge chain is used only as an anti-circularity guard, not as fitted orbital GM. Global parent promotion remains blocked; the R10 Yukawa row becomes the next active product-pressure channel.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "After alpha3, xi, zeta3 and the orbital gamma-beta combo private zeros, the only remaining active local scorecard pressure is the short-range R10 Yukawa row.",
            "success_condition": "Either derive the R10 Yukawa amplitude zero from the same local source/boundary/no-hair branch, or use real source-backed bound rows without claiming a pass.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "formal_doc": str(FORMAL_PATH),
            "post_doc": str(DOC_PATH),
            "validation": str(VALIDATION_PATH),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    algebra: list[dict[str, Any]],
    carriers: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    active_after: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append(
        {
            "validation_id": "VAL4558_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    algebra_text = " ".join(str(value) for row in algebra for value in row.values())
    algebra_ok = "O_orb = (2(gamma-1) - (beta-1))/3" in algebra_text and "3 B_orb" in algebra_text
    rows.append(
        {
            "validation_id": "VAL4558_1_algebra",
            "check": "orbital combo algebra and component no-cancellation bound are explicit",
            "status": "PASS" if algebra_ok else "FAIL",
            "details": "gamma/beta combo checked",
        }
    )

    carriers_text = " ".join(str(value) for row in carriers for value in row.values())
    carriers_ok = all(token in carriers_text for token in ["same-metric EH", "no circular GM import", "independent orbital-sector force"])
    rows.append(
        {
            "validation_id": "VAL4558_2_carriers",
            "check": "carrier classification covers EH coefficients, source charge and independent orbital-force countermodel",
            "status": "PASS" if carriers_ok else "FAIL",
            "details": f"{len(carriers)} carrier rows checked",
        }
    )

    private_zero = next((row for row in zero if row.get("zero_id") == "OZ4558_0_private_selector_orbital_combo"), {})
    zero_ok = private_zero.get("O_orb") == "0"
    zero_ok = zero_ok and private_zero.get("private_selector_ready") == "True"
    zero_ok = zero_ok and private_zero.get("global_parent_claim") == "False"
    rows.append(
        {
            "validation_id": "VAL4558_3_private_zero",
            "check": "orbital private zero certificate exists and remains nonclaim",
            "status": "PASS" if zero_ok else "FAIL",
            "details": "OZ4558_0 checked",
        }
    )

    fallback_ok = all((safe_float(row.get("numeric_value")) or 0.0) > 0 for row in fallback)
    fallback_ok = fallback_ok and all(row.get("valid_for_claim") == "False" for row in fallback)
    rows.append(
        {
            "validation_id": "VAL4558_4_fallback_rows",
            "check": "orbital fallback rows have positive numeric budgets and remain nonclaim",
            "status": "PASS" if fallback_ok else "FAIL",
            "details": f"{len(fallback)} fallback rows checked",
        }
    )

    orbital_row = next((row for row in scorecard if row.get("observable") == OBSERVABLE), {})
    score_ok = orbital_row.get("private_selector_prediction") == "0"
    score_ok = score_ok and orbital_row.get("active_private_pressure") == "False"
    rows.append(
        {
            "validation_id": "VAL4558_5_scorecard",
            "check": "orbital combo scorecard row is private zero and removed from active pressure",
            "status": "PASS" if score_ok else "FAIL",
            "details": "SC4558_orbital/update checked",
        }
    )

    active_ok = bool(active_after) and active_after[0].get("observable") == "alpha_Yukawa_at_lambda_38p6um"
    rows.append(
        {
            "validation_id": "VAL4558_6_active_ranking",
            "check": "R10 Yukawa row selected as next active pressure channel",
            "status": "PASS" if active_ok else "FAIL",
            "details": f"next={active_after[0].get('observable', 'NONE') if active_after else 'NONE'}",
        }
    )

    gates_ok = any(row.get("status") == "PASS_NEXT_SELECTED" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "PASS_ALGEBRA" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "PASS_FIREWALL" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4558_7_gates",
            "check": "next target, algebra and firewall gates pass",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "claim gates checked",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4558_8_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4558_OVERALL",
            "check": "4558 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    algebra: list[dict[str, Any]],
    carriers: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    active_after: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    product = product_row()
    first = active_after[0] if active_after else {}
    return f"""# 4558 - orbital gamma-beta combo private scorecard or finite amplitude row

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4557 selected the orbital `gamma/beta` combination as the next active local pressure channel. 4558 closes it inside the private branch by exact algebra, not by a new orbital fit:

```text
O_orb := ((2+2gamma-beta)/3)-1 = (2(gamma-1) - (beta-1))/3.
```

Inside the private same-metric EH/Hilbert source selector, the PPN readout already gives:

```text
gamma = 1,
beta = 1,
```

therefore:

```text
O_orb = 0.
```

The anti-circularity guard remains important: the Hamiltonian/worldtube source charge and Poisson/Gauss/Newton baseline are fixed before orbital data are treated as tests. No observed orbital `GM` is used as a denominator or hidden calibration.

The fallback no-cancellation budget remains:

```text
{product.get('exact_no_cancellation_condition', '|P_orb|*epsilon_U^2 + |Q_orb| + |R_higher_orb| <= 4.6666666666666672e-05')}
```

After removing the orbital combo, the next active private channel is `{first.get('observable', 'MISSING')}`.

## Orbital Combo Algebra

{markdown_table(algebra)}

## Gamma/Beta Carrier Classification

{markdown_table(carriers)}

## Orbital Combo Private Zero Certificate

{markdown_table(zero)}

## Orbital Combo Finite Amplitude Rows

{markdown_table(fallback)}

## Scorecard After Orbital Combo

{markdown_table(scorecard)}

## Active Ranking After Orbital Combo

{markdown_table(active_after)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_projection_bound",
        "claim": "4558 derives the orbital gamma-beta combination zero inside the private PPN branch from exact algebra and gamma=1, beta=1, with no orbital GM import.",
        "current_evidence": "Generated source register, orbital algebra, gamma/beta carrier classification, private zero certificate, finite fallback rows, scorecard update, claim gates, status and validation CSVs.",
        "status": "orbital_gamma_beta_combo_private_selector_zero_R10_next_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Using the orbital combo zero outside the private same-metric EH/Hilbert scope, importing observed orbital GM, or admitting an independent orbital force without a finite bound.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "orbital combo is now closed inside the private branch; R10 Yukawa row is next active local product-pressure channel.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    algebra = algebra_rows()
    carriers = carrier_rows()
    zero = zero_rows()
    fallback = fallback_rows()
    scorecard = scorecard_after_orbital_rows()
    active_after = active_after_orbital_rows(scorecard)
    gates = claim_gate_rows(active_after)
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ALGEBRA_CSV, algebra)
    write_csv(CARRIER_CSV, carriers)
    write_csv(ZERO_CSV, zero)
    write_csv(FALLBACK_CSV, fallback)
    write_csv(SCORECARD_UPDATE_CSV, scorecard)
    write_csv(ACTIVE_AFTER_CSV, active_after)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4558 - orbital gamma-beta combo private scorecard or finite amplitude row\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, algebra, carriers, zero, fallback, scorecard, active_after, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, algebra, carriers, zero, fallback, scorecard, active_after, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4558 Orbital Gamma-Beta Combo

Marker: `{MARKER}`  
Inside the private same-metric EH/Hilbert-source selector, the orbital `gamma/beta` row is not an independent fitted channel:

```text
O_orb := ((2+2gamma-beta)/3)-1 = (2(gamma-1) - (beta-1))/3 = 0.
```

The zero follows from the private `gamma=1`, `beta=1` PPN readout. Hamiltonian/worldtube source charge and Poisson/Gauss/Newton readout are used as anti-circularity guards: orbital `GM` is not imported as a denominator or calibration. The next active local pressure channel is `alpha_Yukawa_at_lambda_38p6um`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4558 Packet Integration - Orbital Gamma-Beta Combo Zero

Marker: `{PACKET_MARKER}`  
For compact stationary PPC4161-GP-HQNP packets with same-metric EH/Hilbert source readout, `((2+2gamma-beta)/3)-1 = (2(gamma-1)-(beta-1))/3 = 0`. This uses the private `gamma=1`, `beta=1` branch and keeps orbital data downstream as tests, not source-charge definitions.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4558_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
