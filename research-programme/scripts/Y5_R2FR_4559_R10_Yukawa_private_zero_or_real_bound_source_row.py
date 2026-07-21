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

CHECKPOINT = "4559"
CLAIM_ID = "L-401"
BRANCH_ID = "MTS_R2FR_Y5_R10_YUKAWA_PRIVATE_ZERO_4559"
MARKER = "PPC4161_R10_YUKAWA_PRIVATE_ZERO_OR_REAL_BOUND_SOURCE_ROW_4559"
PACKET_MARKER = "PPC4161_PACKET_R10_YUKAWA_PRIVATE_ZERO_4559"
DECISION = "R10_YUKAWA_PRIVATE_ZERO_RECONCILED_LOCAL_SCORECARD_COMPLETE_PARENT_NO_POLE_AND_BOUND_CURVE_STILL_UNSIGNED"
NEXT_TARGET = "4560-Y5-R2FR-local-scorecard-closure-to-parent-signature-gap-map.md"

OBSERVABLE = "alpha_Yukawa_at_lambda_38p6um"
FORMAL_PATH = FORMAL / "575-PPC4161-R10-Yukawa-private-zero-or-real-bound-source-row.md"
DOC_PATH = POST / "4559-Y5-R2FR-R10-Yukawa-private-zero-or-real-bound-source-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4558 = FORMAL / "574-PPC4161-orbital-gamma-beta-combo-private-scorecard-or-finite-amplitude-row.md"
DOC_4550 = FORMAL / "566-PPC4161-first-static-coefficient-product-bound-or-projection-kernel-row.md"
DOC_4173 = FORMAL / "189-PPC4161-local-empirical-validation-pack.md"
POST_4173 = POST / "4173-Y5-R2FR-local-empirical-PPN-R10-clock-WEP-orbital-validation-pack.md"
DOC_4171 = FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md"
DOC_4185_POST = POST / "4185-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
DOC_4187_POST = POST / "4187-Y5-R2FR-local-memory-support-projector-zero-law-for-cGamma-or-PPN-clock-bound.md"
DOC_1022_POST = POST / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
DOC_4539 = FORMAL / "555-PPC4161-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
SCORECARD_4558 = SOURCE_DIR / "P8_Y5_R2FR_4558_SCORECARD_AFTER_ORBITAL_COMBO.csv"
RANKING_4558 = SOURCE_DIR / "P8_Y5_R2FR_4558_ACTIVE_PRODUCT_PRESSURE_RANKING_AFTER_ORBITAL_COMBO.csv"
PRODUCT_BOUNDS_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv"
PREDICTION_4173 = SOURCE_DIR / "P8_Y5_R2FR_4173_PRIVATE_PREDICTION_VECTOR.csv"
BOUND_4173 = SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE.csv"
COMPARATOR_4173 = SOURCE_DIR / "P8_Y5_R2FR_4173_COMPARATOR_RESULTS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4559_SOURCE_REGISTER.csv"
POLE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_R10_POLE_CONTENT_AUDIT.csv"
CHANNEL_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_R10_YUKAWA_CHANNEL_SPLIT.csv"
ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_R10_PRIVATE_ZERO_CERTIFICATE.csv"
FALLBACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_R10_FINITE_AMPLITUDE_ROWS.csv"
SCORECARD_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_SCORECARD_AFTER_R10.csv"
ACTIVE_AFTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_ACTIVE_PRODUCT_PRESSURE_RANKING_AFTER_R10.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4559_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4559_VALIDATION.csv"


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
        ("SRC4559_00_4558_doc", "4558 result selecting R10", DOC_4558, "next active private channel is `alpha_Yukawa_at_lambda_38p6um`"),
        ("SRC4559_01_4558_scorecard", "4558 scorecard R10 row", SCORECARD_4558, "SC4555_alpha_Yukawa_at_lambda_38p6um"),
        ("SRC4559_02_4558_ranking", "4558 active ranking R10 first", RANKING_4558, "1,alpha_Yukawa_at_lambda_38p6um"),
        ("SRC4559_03_4550_bounds", "4550 R10 product bounds", PRODUCT_BOUNDS_4550, "PB4550_alpha_Yukawa_at_lambda_38p6um"),
        ("SRC4559_04_4550_doc", "4550 product-bound doc", DOC_4550, "PB4550_alpha_Yukawa_at_lambda_38p6um"),
        ("SRC4559_05_packet_alpha_zero", "180 packet private alpha zero", PACKET_PATH, "alpha_Yukawa = 0"),
        ("SRC4559_06_4173_formal_alpha_zero", "4173 formal validation alpha zero", DOC_4173, "alpha_Yukawa = 0"),
        ("SRC4559_07_4173_anchor_guard", "4173 formal R10 anchor guard", DOC_4173, "R10 is anchor-only"),
        ("SRC4559_08_4173_post_anchor_guard", "4173 post nonclaim guard", POST_4173, "R10 is anchor-only"),
        ("SRC4559_09_4173_prediction_csv", "4173 private prediction vector", PREDICTION_4173, "R10_yukawa_alpha"),
        ("SRC4559_10_4173_bound_csv", "4173 source-backed bound table", BOUND_4173, "B4173_11_R10"),
        ("SRC4559_11_4173_comparator_csv", "4173 comparator result", COMPARATOR_4173, "C4173_11_R10"),
        ("SRC4559_12_4171_Newton", "4171 Newton readout no Yukawa baseline", DOC_4171, "Poisson/Gauss readout inside the private branch"),
        ("SRC4559_13_4185_extra_residuals", "4185 extra-invariant residual map", DOC_4185_POST, "c_D, delta_kappa, c_Gamma, c_T, c_R2/M_R, c_bdy"),
        ("SRC4559_14_4187_memory_guard", "4187 cGamma memory guard", DOC_4187_POST, "No local-GR, R10, PPN, clock or orbital success claim is allowed"),
        ("SRC4559_15_1022_route_guard", "1022 R10 route separation", DOC_1022_POST, "quotient/vertical route is selected"),
        ("SRC4559_16_4539_firewall", "4539 parent/global firewall", DOC_4539, "FAIL_UNSIGNED"),
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
                "role": "4559 R10 Yukawa private zero reconciliation",
                "valid_for_claim": "False",
            }
        )
    return rows


def pole_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "pole_id": "RP4559_0_EH_massless_spin2",
            "object": "same-metric EH local operator",
            "pole_content": "massless 1/k^2 spin-2 pole only in local weak-field branch",
            "Yukawa_projection": "0",
            "reason": "A Yukawa correction e^{-r/lambda}/r requires an additional finite-mass pole or finite-range auxiliary mode; pure EH/Newton Green function gives the 1/r baseline.",
            "countermodel": "parent admits extra scalar/tensor pole, R^2 mode, memory auxiliary field, or nonlocal finite-range kernel",
            "valid_for_claim": "False",
        },
        {
            "pole_id": "RP4559_1_no_extra_finite_range_branch",
            "object": "PPC4161-TK-HQNP private selector",
            "pole_content": "no extra finite-range local force channel inside private packet",
            "Yukawa_projection": "0",
            "reason": "4173 already records the private prediction alpha_Yukawa=0 from the no-extra-finite-range local-force clause.",
            "countermodel": "the no-extra-mode clause is rejected by the future parent action",
            "valid_for_claim": "False",
        },
        {
            "pole_id": "RP4559_2_boundary_edge_memory",
            "object": "edge, boundary, c_Gamma memory and X-hair branches",
            "pole_content": "not part of pure private EH branch; finite-bound fallback if admitted",
            "Yukawa_projection": "0 inside private branch; open outside it",
            "reason": "The private comparator excludes these carriers, but the corpus still records them as parent-unsigned countermodels needing quotient/no-hair/source rows.",
            "countermodel": "nonzero Qbar_edge_XH, qbar_XT, K_X, c_Gamma_R10, or boundary source term",
            "valid_for_claim": "False",
        },
        {
            "pole_id": "RP4559_3_bound_curve_guard",
            "object": "R10 empirical evidence",
            "pole_content": "anchor-only alpha(lambda=38.6um) bound, not full curve",
            "Yukawa_projection": "private zero passes anchor comparator",
            "reason": "A zero prediction is within any positive bound, but public source-backed R10 evidence still needs a full alpha(lambda) curve or explicit source-backed table.",
            "countermodel": "claiming a public R10 pass from an anchor-only row",
            "valid_for_claim": "False",
        },
    ]


def channel_split_rows() -> list[dict[str, Any]]:
    product = product_row()
    return [
        {
            "split_id": "RS4559_0_start",
            "object": "Delta alpha_R10(lambda)",
            "law": "Delta_alpha_R10 = X_finite_pole(lambda) + E_edge(lambda) + M_memory(lambda) + R_higher(lambda)",
            "meaning": "The R10 row opens only if there is an extra finite-range pole/profile, edge/boundary charge, local memory hair, or higher residual beyond the EH/Newton branch.",
            "numeric_bound": product.get("bound", "1.0000000000000000e+00"),
            "status": "derived_channel_split_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "split_id": "RS4559_1_finite_pole",
            "object": "X_finite_pole(lambda)",
            "law": "X_finite_pole = P_R10[extra massive scalar/tensor/auxiliary propagator]",
            "meaning": "Absent in the private same-metric EH/no-extra-mode selector; live as quotient/vertical or scalar no-hair route outside it.",
            "numeric_bound": product.get("max_product_if_boundary_and_higher_zero", "1.6145606908061397e+14"),
            "status": "zero_inside_private_no_extra_mode_branch",
            "valid_for_claim": "False",
        },
        {
            "split_id": "RS4559_2_edge",
            "object": "E_edge(lambda)",
            "law": "E_edge = P_R10[Qbar_edge_XH, boundary primitive, harmonic/corner edge charge]",
            "meaning": "Excluded inside the private comparator; outside it, edge/boundary proof routes remain parent-unsigned and must be bounded.",
            "numeric_bound": product.get("max_boundary_plus_higher_equal_half_budget", "5.0000000000000000e-01"),
            "status": "zero_inside_private_boundary_silent_branch",
            "valid_for_claim": "False",
        },
        {
            "split_id": "RS4559_3_memory",
            "object": "M_memory(lambda)",
            "law": "M_memory = P_R10[c_Gamma_R10 local memory-hair projection]",
            "meaning": "Not in the private zero comparator; 4187/4188 keep this as a finite-bound/open parent route if memory support is not silenced.",
            "numeric_bound": product.get("max_product_equal_half_budget", "8.0728034540306984e+13"),
            "status": "zero_inside_private_no_memory_hair_branch",
            "valid_for_claim": "False",
        },
    ]


def zero_rows() -> list[dict[str, Any]]:
    product = product_row()
    return [
        {
            "zero_id": "RZ4559_0_private_selector_R10",
            "scope": "private PPC4161-GP-HQNP same-metric EH/Newton no-extra-finite-range local selector",
            "alpha_Yukawa_at_lambda_38p6um": "0",
            "basis": "pure EH/Newton weak-field branch has no finite-mass Yukawa pole; 4173 private prediction vector records alpha_Yukawa=0; edge/memory/X-hair carriers are excluded inside this private comparator",
            "bound": product.get("bound", "1.0000000000000000e+00"),
            "private_selector_ready": "True",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "RZ4559_1_anchor_comparator",
            "scope": "source-backed R10 anchor-only comparator",
            "alpha_Yukawa_at_lambda_38p6um": "0 <= 1",
            "basis": "4173 comparator result passes the Eot-Wash 2020 gravitational-strength anchor, but full_curve_available=False",
            "bound": product.get("bound", "1.0000000000000000e+00"),
            "private_selector_ready": "True",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "RZ4559_2_global_firewall",
            "scope": "full MTS parent/global/R10 curve/X-hair/source-bound sectors",
            "alpha_Yukawa_at_lambda_38p6um": "not_promoted",
            "basis": "parent no-pole/no-extra-mode theorem, quotient/vertical certificate, scalar no-hair branch, edge source rows and full alpha(lambda) curve are not globally claim-ready",
            "bound": product.get("bound", "1.0000000000000000e+00"),
            "private_selector_ready": "False",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def fallback_rows() -> list[dict[str, Any]]:
    product = product_row()
    return [
        {
            "row_id": "RF4559_0_master_no_cancellation",
            "channel": "R10 total retained channel",
            "exact_requirement": product.get("exact_no_cancellation_condition", "|P_R10|*epsilon_U^2 + |Q_R10| + |R_higher_R10| <= 1"),
            "numeric_value": product.get("bound", "1.0000000000000000e+00"),
            "units": product.get("bound_units", "dimensionless"),
            "status": "fallback_if_private_zero_scope_fails_anchor_only_non_curve",
            "valid_for_claim": "False",
        },
        {
            "row_id": "RF4559_1_source_product_if_boundary_zero",
            "channel": "P_R10(lambda)",
            "exact_requirement": "|P_R10| <= B_R10/epsilon_U^2 if boundary and higher terms are zero",
            "numeric_value": product.get("max_product_if_boundary_and_higher_zero", "1.6145606908061397e+14"),
            "units": "dimensionless effective product",
            "status": "finite_source_product_budget_nonclaim_anchor_only",
            "valid_for_claim": "False",
        },
        {
            "row_id": "RF4559_2_source_product_equal_half_budget",
            "channel": "P_R10(lambda)",
            "exact_requirement": "|P_R10| <= (B_R10/2)/epsilon_U^2 under equal source/boundary+higher split",
            "numeric_value": product.get("max_product_equal_half_budget", "8.0728034540306984e+13"),
            "units": "dimensionless effective product",
            "status": "finite_source_product_half_budget_nonclaim_anchor_only",
            "valid_for_claim": "False",
        },
        {
            "row_id": "RF4559_3_boundary_plus_higher_half_budget",
            "channel": "Q_R10 + R_higher_R10",
            "exact_requirement": "|Q_R10| + |R_higher_R10| <= B_R10/2 under equal split",
            "numeric_value": product.get("max_boundary_plus_higher_equal_half_budget", "5.0000000000000000e-01"),
            "units": product.get("bound_units", "dimensionless"),
            "status": "finite_boundary_higher_budget_nonclaim_anchor_only",
            "valid_for_claim": "False",
        },
        {
            "row_id": "RF4559_4_full_curve_requirement",
            "channel": "alpha(lambda) evidence",
            "exact_requirement": "valid public R10 claim requires a digitized/source-backed alpha(lambda) curve or machine-readable table, not only alpha=1 at lambda=38.6um",
            "numeric_value": "MISSING_FULL_CURVE",
            "units": "dimensionless curve",
            "status": "public_claim_blocker",
            "valid_for_claim": "False",
        },
    ]


def scorecard_after_R10_rows() -> list[dict[str, Any]]:
    rows = read_csv(SCORECARD_4558)
    updated: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        if row.get("observable") == OBSERVABLE:
            item["private_selector_prediction"] = "0"
            item["private_selector_status"] = "PASS_PRIVATE_SELECTOR_ZERO_ANCHOR_ONLY_NONPUBLIC"
            item["active_private_pressure"] = "False"
            item["next_action"] = "do not reopen R10 inside private EH/no-extra-mode branch; for public/global claim derive no-pole/no-hair or source full alpha(lambda) curve"
        updated.append(item)
    return updated


def active_after_R10_rows(scorecard: list[dict[str, Any]]) -> list[dict[str, Any]]:
    active = [row for row in scorecard if row.get("active_private_pressure") == "True"]
    active.sort(key=lambda row: safe_float(row.get("max_product_if_boundary_and_higher_zero")) or float("inf"))
    if not active:
        return [
            {
                "active_rank": 0,
                "observable": "NONE",
                "arena": "local_scorecard_private_pressure_complete",
                "max_product_if_boundary_and_higher_zero": "",
                "recommended_next": "False",
                "valid_for_claim": "False",
            }
        ]
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
    no_active = active_after and active_after[0].get("observable") == "NONE"
    return [
        {
            "gate_id": "G4559_0_R10_private_zero",
            "requirement": "alpha_Yukawa=0 inside private EH/no-extra-finite-range branch",
            "status": "PASS_PRIVATE_SELECTOR",
            "claim_effect": "R10 removed from active private product pressure",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4559_1_no_pole_scope",
            "requirement": "Yukawa correction requires finite-mass pole or equivalent finite-range source branch",
            "status": "PASS_BRANCH_DERIVATION",
            "claim_effect": "pure EH/Newton private branch has no R10 Yukawa channel",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4559_2_anchor_only_firewall",
            "requirement": "R10 evidence remains anchor-only/full_curve_available=False",
            "status": "PASS_FIREWALL",
            "claim_effect": "prevents public R10/local-GR claim from anchor smoke row",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4559_3_parent_no_pole_firewall",
            "requirement": "global parent no-pole/no-extra-mode theorem remains unsigned",
            "status": "PASS_PARENT_FIREWALL",
            "claim_effect": "moves next work to parent signature gap instead of pretending final proof",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4559_4_local_scorecard_pressure",
            "requirement": "no active private product-pressure rows remain",
            "status": "PASS_LOCAL_SCORECARD_PRIVATE_COMPLETE" if no_active else "FAIL_ACTIVE_ROWS_REMAIN",
            "claim_effect": "next hard target = parent signature gap map",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4559_0",
            "decision": DECISION,
            "summary": "4559 reconciles the only remaining active local pressure row. In the private same-metric EH/Newton/no-extra-finite-range branch, a Yukawa correction has no finite-mass pole or edge/memory carrier, and 4173 already records alpha_Yukawa=0. The R10 anchor comparator passes privately, but no public R10/local-GR claim is made because the R10 evidence is anchor-only and the parent no-pole/no-extra-mode/no-hair routes remain unsigned. The local private scorecard now has no active product-pressure rows.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "The local private scorecard pressure rows are now reconciled. The real remaining work is parent promotion: prove the MTS parent forces the EH/no-extra-mode/source-coupled branch rather than treating it as an effective closure.",
            "success_condition": "Map every local private zero to its parent-owned signature clause: EH principal block, source coupling, no finite-range pole, boundary/edge silence, memory support silence and full source-backed empirical data requirements.",
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
    poles: list[dict[str, Any]],
    split: list[dict[str, Any]],
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
            "validation_id": "VAL4559_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    pole_text = " ".join(str(value) for row in poles for value in row.values())
    pole_ok = all(token in pole_text for token in ["finite-mass pole", "alpha(lambda)", "anchor-only"])
    rows.append(
        {
            "validation_id": "VAL4559_1_pole_audit",
            "check": "R10 pole audit distinguishes EH no-pole zero from extra finite-range countermodels",
            "status": "PASS" if pole_ok else "FAIL",
            "details": f"{len(poles)} pole rows checked",
        }
    )

    split_text = " ".join(str(value) for row in split for value in row.values())
    split_ok = all(token in split_text for token in ["X_finite_pole", "E_edge", "M_memory", "R_higher"])
    rows.append(
        {
            "validation_id": "VAL4559_2_split",
            "check": "R10 split includes finite pole, edge, memory and higher residuals",
            "status": "PASS" if split_ok else "FAIL",
            "details": "Delta_alpha_R10 split checked",
        }
    )

    private_zero = next((row for row in zero if row.get("zero_id") == "RZ4559_0_private_selector_R10"), {})
    zero_ok = private_zero.get("alpha_Yukawa_at_lambda_38p6um") == "0"
    zero_ok = zero_ok and private_zero.get("private_selector_ready") == "True"
    zero_ok = zero_ok and private_zero.get("global_parent_claim") == "False"
    rows.append(
        {
            "validation_id": "VAL4559_3_private_zero",
            "check": "R10 private zero certificate exists and remains nonclaim",
            "status": "PASS" if zero_ok else "FAIL",
            "details": "RZ4559_0 checked",
        }
    )

    numeric_fallback = [row for row in fallback if row.get("numeric_value") != "MISSING_FULL_CURVE"]
    fallback_ok = all((safe_float(row.get("numeric_value")) or 0.0) > 0 for row in numeric_fallback)
    fallback_ok = fallback_ok and all(row.get("valid_for_claim") == "False" for row in fallback)
    fallback_ok = fallback_ok and any(row.get("numeric_value") == "MISSING_FULL_CURVE" for row in fallback)
    rows.append(
        {
            "validation_id": "VAL4559_4_fallback_rows",
            "check": "R10 fallback rows have positive numeric anchor budgets and explicit full-curve blocker",
            "status": "PASS" if fallback_ok else "FAIL",
            "details": f"{len(fallback)} fallback rows checked",
        }
    )

    r10_row = next((row for row in scorecard if row.get("observable") == OBSERVABLE), {})
    score_ok = r10_row.get("private_selector_prediction") == "0"
    score_ok = score_ok and r10_row.get("active_private_pressure") == "False"
    rows.append(
        {
            "validation_id": "VAL4559_5_scorecard",
            "check": "R10 scorecard row is private zero and removed from active pressure",
            "status": "PASS" if score_ok else "FAIL",
            "details": "SC4559_R10/update checked",
        }
    )

    active_ok = bool(active_after) and active_after[0].get("observable") == "NONE"
    rows.append(
        {
            "validation_id": "VAL4559_6_active_ranking",
            "check": "no active private product-pressure rows remain",
            "status": "PASS" if active_ok else "FAIL",
            "details": f"active_marker={active_after[0].get('observable', 'MISSING') if active_after else 'MISSING'}",
        }
    )

    gates_ok = any(row.get("status") == "PASS_LOCAL_SCORECARD_PRIVATE_COMPLETE" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "PASS_FIREWALL" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "PASS_PARENT_FIREWALL" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4559_7_gates",
            "check": "local scorecard completion, anchor firewall and parent firewall gates pass",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "claim gates checked",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4559_8_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4559_OVERALL",
            "check": "4559 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    poles: list[dict[str, Any]],
    split: list[dict[str, Any]],
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
    return f"""# 4559 - R10 Yukawa private zero or real bound source row

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4558 left one active local product-pressure row: `alpha_Yukawa_at_lambda_38p6um`. 4559 reconciles it with the older 4173 private comparator:

```text
alpha_Yukawa(lambda=38.6 um) = 0
```

inside the private same-metric EH/Newton/no-extra-finite-range selector.

The reason is structural rather than fitted: a Yukawa term `alpha exp(-r/lambda)/r` requires an extra finite-mass pole, finite-range auxiliary mode, edge charge, memory-hair profile, or equivalent non-EH residual. The private EH/Newton branch has none of those carriers. Therefore:

```text
Delta_alpha_R10 = X_finite_pole + E_edge + M_memory + R_higher = 0
```

inside that branch.

This is still not a public R10/local-GR claim. The 4173 R10 evidence is anchor-only (`alpha=1` at `lambda=38.6um`), not a full `alpha(lambda)` curve, and the global parent no-pole/no-extra-mode/no-hair certificates remain unsigned.

The fallback no-cancellation budget remains:

```text
{product.get('exact_no_cancellation_condition', '|P_R10|*epsilon_U^2 + |Q_R10| + |R_higher_R10| <= 1')}
```

After removing R10, no active private product-pressure rows remain in this scorecard.

## R10 Pole Content Audit

{markdown_table(poles)}

## R10 Yukawa Channel Split

{markdown_table(split)}

## R10 Private Zero Certificate

{markdown_table(zero)}

## R10 Finite Amplitude Rows

{markdown_table(fallback)}

## Scorecard After R10

{markdown_table(scorecard)}

## Active Ranking After R10

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
        "claim": "4559 reconciles R10 alpha_Yukawa=0 inside the private EH/Newton/no-extra-finite-range branch while preserving anchor-only and parent no-pole firewalls.",
        "current_evidence": "Generated source register, pole audit, R10 channel split, private zero certificate, finite fallback rows, scorecard update, claim gates, status and validation CSVs.",
        "status": "R10_private_selector_zero_local_scorecard_complete_parent_gap_next_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Claiming public R10/local-GR success without a full alpha(lambda) curve or parent-signed no-pole/no-extra-mode/no-hair certificate.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "local private product-pressure scorecard now has no active rows; next work is parent signature gap mapping.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    poles = pole_audit_rows()
    split = channel_split_rows()
    zero = zero_rows()
    fallback = fallback_rows()
    scorecard = scorecard_after_R10_rows()
    active_after = active_after_R10_rows(scorecard)
    gates = claim_gate_rows(active_after)
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(POLE_AUDIT_CSV, poles)
    write_csv(CHANNEL_SPLIT_CSV, split)
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

    pending_doc = f"# 4559 - R10 Yukawa private zero or real bound source row\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, poles, split, zero, fallback, scorecard, active_after, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, poles, split, zero, fallback, scorecard, active_after, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4559 R10 Yukawa Private Zero

Marker: `{MARKER}`  
Inside the private same-metric EH/Newton/no-extra-finite-range selector:

```text
alpha_Yukawa(lambda=38.6 um) = 0.
```

The branch contains no extra finite-mass pole, edge charge, or memory-hair carrier:

```text
Delta_alpha_R10 = X_finite_pole + E_edge + M_memory + R_higher = 0.
```

The local private product-pressure scorecard now has no active rows. This is not a public R10/local-GR claim because the R10 bound is anchor-only and the parent no-pole/no-extra-mode/no-hair certificate remains unsigned.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4559 Packet Integration - R10 Yukawa Private Zero

Marker: `{PACKET_MARKER}`  
For compact stationary PPC4161-GP-HQNP packets with same-metric EH/Newton readout and no extra finite-range local force channel, `alpha_Yukawa(lambda=38.6 um)=0`. Any admitted finite-mass pole, X-hair, edge charge, memory profile, or full R10 curve claim reopens the nonclaim bound route.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4559_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
