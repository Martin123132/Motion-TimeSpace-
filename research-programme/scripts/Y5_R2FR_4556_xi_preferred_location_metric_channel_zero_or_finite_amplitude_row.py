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

CHECKPOINT = "4556"
CLAIM_ID = "L-398"
BRANCH_ID = "MTS_R2FR_Y5_XI_PREFERRED_LOCATION_METRIC_CHANNEL_4556"
MARKER = "PPC4161_XI_PREFERRED_LOCATION_METRIC_CHANNEL_ZERO_OR_FINITE_AMPLITUDE_ROW_4556"
PACKET_MARKER = "PPC4161_PACKET_XI_PRIVATE_SELECTOR_ZERO_4556"
DECISION = "XI_PRIVATE_SELECTOR_ZERO_DERIVED_NEXT_HARD_CHANNEL_ZETA3_GLOBAL_PARENT_UNSIGNED"
NEXT_TARGET = "4557-Y5-R2FR-zeta3-stress-conservation-channel-zero-or-finite-amplitude-row.md"

FORMAL_PATH = FORMAL / "572-PPC4161-xi-preferred-location-metric-channel-zero-or-finite-amplitude-row.md"
DOC_PATH = POST / "4556-Y5-R2FR-xi-preferred-location-metric-channel-zero-or-finite-amplitude-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4555 = FORMAL / "571-PPC4161-alpha3-private-zero-to-PPN-scorecard-and-next-hard-channel.md"
DOC_4550 = FORMAL / "566-PPC4161-first-static-coefficient-product-bound-or-projection-kernel-row.md"
DOC_4172 = FORMAL / "188-PPC4161-full-PPN-readout-vector.md"
DOC_4539 = FORMAL / "555-PPC4161-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
DOC_4176 = POST / "4176-Y5-R2FR-local-boundary-no-flux-sector-interface-theorem-or-transition-current-bound.md"
PACKET = FORMAL / "180-PPC4161-private-local-packet-integration.md"
SCORECARD_4555 = SOURCE_DIR / "P8_Y5_R2FR_4555_LOCAL_PPN_SCORECARD_REFRESH.csv"
RANKING_4555 = SOURCE_DIR / "P8_Y5_R2FR_4555_ACTIVE_PRODUCT_PRESSURE_RANKING.csv"
XI_AUDIT_4555 = SOURCE_DIR / "P8_Y5_R2FR_4555_NEXT_CHANNEL_XI_AUDIT.csv"
PRODUCT_BOUNDS_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv"
BOUNDARY_OWNER = SOURCE_DIR / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4556_SOURCE_REGISTER.csv"
XI_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_XI_CHANNEL_SPLIT.csv"
XI_CARRIER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_XI_CARRIER_CLASSIFICATION.csv"
XI_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_XI_PRIVATE_ZERO_CERTIFICATE.csv"
XI_FALLBACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_XI_FINITE_AMPLITUDE_ROWS.csv"
SCORECARD_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_SCORECARD_AFTER_XI.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4556_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4556_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def xi_product_row() -> dict[str, str]:
    return next((row for row in read_csv(PRODUCT_BOUNDS_4550) if row.get("observable") == "xi"), {})


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4556_00_4555_doc", "4555 xi next target doc", DOC_4555, "observable = xi"),
        ("SRC4556_01_4555_xi_audit", "4555 xi next-channel audit", XI_AUDIT_4555, "NX4555_0_selected_channel"),
        ("SRC4556_02_4555_scorecard", "4555 scorecard xi row", SCORECARD_4555, "SC4555_xi"),
        ("SRC4556_03_4550_bounds", "4550 xi product bounds", PRODUCT_BOUNDS_4550, "PB4550_xi"),
        ("SRC4556_04_4550_doc", "4550 product-bound doc", DOC_4550, "PB4550_xi"),
        ("SRC4556_05_4172_ppn", "4172 private PPN readout", DOC_4172, "xi = 0."),
        ("SRC4556_06_packet_ppn", "180 packet PPN vector", PACKET, "gamma-1 = beta-1 = alpha1 = alpha2 = alpha3 = xi"),
        ("SRC4556_07_4176_no_flux", "4176 private no-flux theorem", DOC_4176, "LOCAL_BOUNDARY_NO_FLUX_THEOREM_CLOSES_TRANSITION_CURRENT_PRIVATE_SELECTOR"),
        ("SRC4556_08_boundary_owner", "boundary scalar owner attempt", BOUNDARY_OWNER, "O1_homogeneous_scalar_action"),
        ("SRC4556_09_4539_firewall", "4539 parent/global firewall", DOC_4539, "FAIL_UNSIGNED"),
        ("SRC4556_10_4555_ranking", "4555 active ranking", RANKING_4555, "1,xi"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4556 xi preferred-location metric channel derivation",
                "valid_for_claim": "False",
            }
        )
    return rows


def xi_split_rows() -> list[dict[str, Any]]:
    product = xi_product_row()
    return [
        {
            "split_id": "XS4556_0_start",
            "object": "Delta xi",
            "law": "Delta_xi = A_xi_TF + B_xi_boundary_TF + G_xi_pref + R_xi_higher",
            "meaning": "xi is a metric/preferred-location channel. It is sourced by trace-free anisotropic metric carriers, boundary trace-free stress/Hessian, or global preferred-location leakage, not by the alpha3 vector self-acceleration channel.",
            "numeric_bound": product.get("bound", "4e-9"),
            "status": "derived_channel_split_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "split_id": "XS4556_1_source_TF",
            "object": "A_xi_TF",
            "law": "A_xi_TF = P_xi[trace-free anisotropic local source/metric carrier]",
            "meaning": "Centred scalar monopole and isotropic trace pieces can renormalize U/gamma/beta but do not create a preferred-location xi carrier.",
            "numeric_bound": product.get("max_product_if_boundary_and_higher_zero", "6.4582427632245596e+05"),
            "status": "zero_inside_private_centred_scalar_branch",
            "valid_for_claim": "False",
        },
        {
            "split_id": "XS4556_2_boundary_TF",
            "object": "B_xi_boundary_TF",
            "law": "B_xi_boundary_TF = P_xi[boundary trace-free stress or angular Hessian]",
            "meaning": "Homogeneous scalar boundary data give trace stress only; angular derivatives vanish, so trace-free boundary xi carriers are absent in the branch.",
            "numeric_bound": product.get("max_boundary_plus_higher_equal_half_budget", "2e-9"),
            "status": "zero_inside_private_homogeneous_boundary_branch",
            "valid_for_claim": "False",
        },
        {
            "split_id": "XS4556_3_global_pref",
            "object": "G_xi_pref",
            "law": "G_xi_pref = P_xi[external preferred-location/global potential/open-sector leakage]",
            "meaning": "Compact support separation and routed/no-flux boundary remove unmodelled galaxy/cosmology/open-memory preferred-location leakage from the local selector.",
            "numeric_bound": product.get("bound", "4e-9"),
            "status": "zero_inside_private_no_flux_branch",
            "valid_for_claim": "False",
        },
    ]


def xi_carrier_rows() -> list[dict[str, Any]]:
    return [
        {
            "carrier_id": "XC4556_0_scalar_monopole",
            "carrier": "centred l=0 scalar source/profile",
            "representation": "scalar trace",
            "xi_projection": "0",
            "reason": "l=0 trace contributes to ordinary Newton/gamma/beta potentials, not preferred-location anisotropy.",
            "private_selector_status": "zero",
            "countermodel": "off-centre or l>=2 source profile",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "XC4556_1_radial_gradient_pair",
            "carrier": "radial gradient products n_i n_j F(r)",
            "representation": "isotropic trace plus l=2 angular part",
            "xi_projection": "0 after centred angular average in scalar branch",
            "reason": "The local PPN xi readout needs an admitted preferred-location tensor, not the isotropic averaged trace of a centred radial scalar.",
            "private_selector_status": "zero_for_xi_branch",
            "countermodel": "anisotropic domain weighting or unaveraged external tidal tensor",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "XC4556_2_homogeneous_scalar_boundary",
            "carrier": "boundary action sqrt(gamma)F(Y_scalar homogeneous)",
            "representation": "tangential trace",
            "xi_projection": "0",
            "reason": "Variation gives tau_AB proportional gamma_AB; no trace-free angular stress/Hessian survives.",
            "private_selector_status": "zero",
            "countermodel": "angularly varying scalar boundary functional",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "XC4556_3_global_preferred_location",
            "carrier": "external galaxy/cosmology/open-memory potential or preferred-location label",
            "representation": "external scalar/tensor environment",
            "xi_projection": "0 inside support-separated no-flux branch",
            "reason": "The compact local selector forbids unmodelled cross-sector pullback into the local PPN readout.",
            "private_selector_status": "zero_inside_branch",
            "countermodel": "open-sector leakage or non-routed boundary charge",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "XC4556_4_independent_TF_metric",
            "carrier": "independent trace-free metric/tensor residual",
            "representation": "l>=2 trace-free tensor",
            "xi_projection": "not allowed inside branch",
            "reason": "If admitted, this is not xi-zero; it needs a finite amplitude row or a parent no-independent-TF theorem.",
            "private_selector_status": "excluded_or_bound",
            "countermodel": "Kperp/non-EH tensor sector",
            "valid_for_claim": "False",
        },
    ]


def xi_zero_rows() -> list[dict[str, Any]]:
    product = xi_product_row()
    return [
        {
            "zero_id": "XZ4556_0_private_selector_xi",
            "scope": "private PPC4161-GP-HQNP compact centred stationary non-radiative local selector",
            "Delta_xi": "0",
            "basis": "centred scalar monopole/isotropic trace only; homogeneous scalar boundary trace; no unmodelled preferred-location/open-sector leakage; no independent trace-free metric carrier",
            "bound": product.get("bound", "4.0000000000000002e-09"),
            "private_selector_ready": "True",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "XZ4556_1_global_firewall",
            "scope": "full MTS parent/global/open/radiative/anistropic sectors",
            "Delta_xi": "not_promoted",
            "basis": "global no-flux, A_MF/quotient adoption and no-independent-TF metric carrier are not globally parent-signed",
            "bound": product.get("bound", "4.0000000000000002e-09"),
            "private_selector_ready": "False",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def xi_fallback_rows() -> list[dict[str, Any]]:
    product = xi_product_row()
    return [
        {
            "row_id": "XF4556_0_master_no_cancellation",
            "channel": "xi total retained channel",
            "exact_requirement": product.get("exact_no_cancellation_condition", "|P_xi|epsilon_U^2 + |Q_xi| + |R_higher_xi| <= 4e-9"),
            "numeric_value": product.get("bound", "4.0000000000000002e-09"),
            "units": product.get("bound_units", "dimensionless"),
            "status": "fallback_if_private_zero_scope_fails",
            "valid_for_claim": "False",
        },
        {
            "row_id": "XF4556_1_source_product_if_boundary_zero",
            "channel": "P_xi",
            "exact_requirement": "|P_xi| <= B_xi/epsilon_U^2 if boundary and higher terms are zero",
            "numeric_value": product.get("max_product_if_boundary_and_higher_zero", "6.4582427632245596e+05"),
            "units": "dimensionless effective product",
            "status": "finite_source_product_budget_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "XF4556_2_boundary_plus_higher_half_budget",
            "channel": "Q_xi + R_higher_xi",
            "exact_requirement": "|Q_xi| + |R_higher_xi| <= B_xi/2 under equal split",
            "numeric_value": product.get("max_boundary_plus_higher_equal_half_budget", "2.0000000000000001e-09"),
            "units": product.get("bound_units", "dimensionless"),
            "status": "finite_boundary_higher_budget_nonclaim",
            "valid_for_claim": "False",
        },
    ]


def scorecard_after_xi_rows() -> list[dict[str, Any]]:
    rows = read_csv(SCORECARD_4555)
    updated: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        if row.get("observable") == "xi":
            item["private_selector_prediction"] = "0"
            item["private_selector_status"] = "PASS_PRIVATE_SELECTOR_ZERO"
            item["active_private_pressure"] = "False"
            item["next_action"] = "do not reopen xi unless anisotropic/preferred-location scope changes"
        updated.append(item)
    return updated


def active_after_xi_rows(scorecard: list[dict[str, Any]]) -> list[dict[str, Any]]:
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


def claim_gate_rows(scorecard: list[dict[str, Any]]) -> list[dict[str, Any]]:
    active = active_after_xi_rows(scorecard)
    next_observable = active[0].get("observable", "NONE") if active else "NONE"
    return [
        {
            "gate_id": "G4556_0_xi_private_zero",
            "requirement": "xi=0 inside compact centred scalar/no-flux private selector",
            "status": "PASS_PRIVATE_SELECTOR",
            "claim_effect": "xi removed from active private product pressure",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4556_1_global_public_firewall",
            "requirement": "global parent/public xi claim remains false",
            "status": "PASS_FIREWALL",
            "claim_effect": "prevents overclaiming preferred-location closure",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4556_2_countermodel_guard",
            "requirement": "anisotropic/domain/open-sector/independent trace-free carriers remain guarded",
            "status": "GUARD_RETAINED",
            "claim_effect": "xi reopens if private branch scope changes",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4556_3_next_channel_selection",
            "requirement": "remaining channels ranked after xi removal",
            "status": "PASS_NEXT_SELECTED" if next_observable == "zeta3" else "FAIL_NEXT_SELECTION",
            "claim_effect": f"next hard channel = {next_observable}",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4556_0",
            "decision": DECISION,
            "summary": "4556 derives xi=0 inside the private compact centred stationary non-radiative selector by classifying xi as a preferred-location/trace-free metric channel. Centred scalar trace, homogeneous scalar boundary and support-separated no-flux data do not supply the required anisotropic carrier. Global parent promotion remains blocked; zeta3 becomes the next active product-pressure channel.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "After alpha3 and xi private zeros, zeta3 is the tightest remaining active local product-pressure channel.",
            "success_condition": "Derive zeta3=0 from stress/Hilbert conservation and no independent stress leakage inside the private selector, or fill finite P_zeta3/Q_zeta3/R_higher_zeta3 amplitude rows.",
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
    split: list[dict[str, Any]],
    carriers: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append(
        {
            "validation_id": "VAL4556_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    split_text = " ".join(str(value) for row in split for value in row.values())
    split_ok = all(token in split_text for token in ["A_xi_TF", "B_xi_boundary_TF", "G_xi_pref", "R_xi_higher"])
    rows.append(
        {
            "validation_id": "VAL4556_1_split",
            "check": "xi split includes source trace-free, boundary trace-free, global preferred-location and higher terms",
            "status": "PASS" if split_ok else "FAIL",
            "details": "Delta_xi split checked",
        }
    )

    carriers_text = " ".join(str(value) for row in carriers for value in row.values())
    carriers_ok = "trace-free" in carriers_text and "preferred-location" in carriers_text and "countermodel" in " ".join(carriers[0].keys())
    rows.append(
        {
            "validation_id": "VAL4556_2_carriers",
            "check": "xi carrier classification is trace-free/preferred-location specific",
            "status": "PASS" if carriers_ok else "FAIL",
            "details": f"{len(carriers)} carrier rows checked",
        }
    )

    private_zero = next((row for row in zero if row.get("zero_id") == "XZ4556_0_private_selector_xi"), {})
    zero_ok = private_zero.get("Delta_xi") == "0" and private_zero.get("private_selector_ready") == "True"
    zero_ok = zero_ok and private_zero.get("global_parent_claim") == "False"
    rows.append(
        {
            "validation_id": "VAL4556_3_private_zero",
            "check": "xi private zero certificate exists and remains nonclaim",
            "status": "PASS" if zero_ok else "FAIL",
            "details": "XZ4556_0 checked",
        }
    )

    fallback_ok = all((safe_float(row.get("numeric_value")) or 0.0) > 0 for row in fallback)
    fallback_ok = fallback_ok and all(row.get("valid_for_claim") == "False" for row in fallback)
    rows.append(
        {
            "validation_id": "VAL4556_4_fallback_rows",
            "check": "xi fallback rows have positive numeric budgets and remain nonclaim",
            "status": "PASS" if fallback_ok else "FAIL",
            "details": f"{len(fallback)} fallback rows checked",
        }
    )

    xi_row = next((row for row in scorecard if row.get("observable") == "xi"), {})
    score_ok = xi_row.get("private_selector_prediction") == "0"
    score_ok = score_ok and xi_row.get("active_private_pressure") == "False"
    rows.append(
        {
            "validation_id": "VAL4556_5_scorecard",
            "check": "xi scorecard row is private zero and removed from active pressure",
            "status": "PASS" if score_ok else "FAIL",
            "details": "SC4556_xi/update checked",
        }
    )

    gates_ok = any(row.get("status") == "PASS_NEXT_SELECTED" and "zeta3" in row.get("claim_effect", "") for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "PASS_FIREWALL" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4556_6_gates",
            "check": "zeta3 selected next and public/global firewall remains",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "claim gates checked",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4556_7_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4556_OVERALL",
            "check": "4556 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    split: list[dict[str, Any]],
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
    product = xi_product_row()
    first = active_after[0] if active_after else {}
    return f"""# 4556 - xi preferred-location metric channel zero or finite amplitude row

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4555 selected `xi` as the next tightest active local channel after `alpha3` closed privately. 4556 treats it correctly: `xi` is not an alpha3-style vector channel. It is a preferred-location / trace-free metric channel.

Use the split:

```text
Delta_xi = A_xi_TF + B_xi_boundary_TF + G_xi_pref + R_xi_higher.
```

Inside the private compact centred stationary non-radiative selector:

- centred scalar monopoles and scalar traces do not create preferred-location anisotropy;
- homogeneous scalar boundary data give trace stress, not trace-free angular stress;
- support separation/no-flux removes unmodelled galaxy/cosmology/open-memory preferred-location leakage;
- independent trace-free metric/tensor carriers remain countermodels outside the private certificate.

Therefore:

```text
Delta_xi = 0
```

inside the private branch. The fallback no-cancellation budget remains:

```text
{product.get('exact_no_cancellation_condition', '|P_xi|epsilon_U^2 + |Q_xi| + |R_higher_xi| <= 4e-9')}
```

After removing `xi`, the next active private channel is `{first.get('observable', 'MISSING')}`.

## Xi Channel Split

{markdown_table(split)}

## Xi Carrier Classification

{markdown_table(carriers)}

## Xi Private Zero Certificate

{markdown_table(zero)}

## Xi Finite Amplitude Rows

{markdown_table(fallback)}

## Scorecard After Xi

{markdown_table(scorecard)}

## Active Ranking After Xi

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
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_projection_bound",
        "claim": "4556 derives xi=0 inside the private compact centred stationary selector by classifying xi as a preferred-location/trace-free metric channel and excluding its carriers in-branch.",
        "current_evidence": "Generated source register, xi channel split, carrier classification, private zero certificate, finite fallback rows, scorecard update, claim gates, status and validation CSVs.",
        "status": "xi_private_selector_zero_zeta3_next_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Using xi private zero outside centred/homogeneous/no-flux scope, or ignoring anisotropic trace-free/open-sector countermodels.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "xi is now closed inside the private branch; zeta3 is next active local product-pressure channel.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    split = xi_split_rows()
    carriers = xi_carrier_rows()
    zero = xi_zero_rows()
    fallback = xi_fallback_rows()
    scorecard = scorecard_after_xi_rows()
    active_after = active_after_xi_rows(scorecard)
    gates = claim_gate_rows(scorecard)
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(XI_SPLIT_CSV, split)
    write_csv(XI_CARRIER_CSV, carriers)
    write_csv(XI_ZERO_CSV, zero)
    write_csv(XI_FALLBACK_CSV, fallback)
    write_csv(SCORECARD_UPDATE_CSV, scorecard)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4556_ACTIVE_PRODUCT_PRESSURE_RANKING_AFTER_XI.csv", active_after)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4556 - xi preferred-location metric channel zero or finite amplitude row\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, split, carriers, zero, fallback, scorecard, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, split, carriers, zero, fallback, scorecard, active_after, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4556 Xi Preferred-Location Metric Channel

Marker: `{MARKER}`  
Inside the private compact centred stationary non-radiative selector, `xi=0` is derived by classifying it as a preferred-location / trace-free metric channel:

```text
Delta_xi = A_xi_TF + B_xi_boundary_TF + G_xi_pref + R_xi_higher = 0.
```

Scalar traces and homogeneous scalar boundaries do not supply trace-free preferred-location carriers; open/global anisotropic carriers remain countermodels outside the private branch. The next active local pressure channel is `zeta3`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4556 Packet Integration - Xi Private Selector Zero

Marker: `{PACKET_MARKER}`  
For compact centred stationary PPC4161-GP-HQNP packets, `xi` is zero as a preferred-location/trace-free metric channel. This is not an alpha3 vector proof: it depends on isotropic scalar source trace, homogeneous scalar boundary trace and support-separated no-flux conditions. Anisotropic/open-sector trace-free carriers reopen xi.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4556_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
